"""
O.N.E. — Supabase Auth Sync Migration
======================================
Idempotent script that:
  1. Backfills auth.users + auth.identities from public.users (preserving exact UUIDs & bcrypt hashes).
  2. Creates a trigger to auto-sync any future Supabase Auth sign-ups into public.users.
  3. Enables RLS on all public tables with backend-safe + per-user + admin policies.
  4. Runs 4 verification checkpoints and prints a confirmation log.

Run from backend/ directory:
    python supabase_auth_sync.py
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# ─── Load .env ───────────────────────────────────────────────────────────────
load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("FATAL: DATABASE_URL is missing from .env. Aborting.")
    sys.exit(1)

print("=" * 60)
print("  O.N.E. Supabase Auth Sync Migration")
print("=" * 60)
host = DATABASE_URL.split("@")[-1].split("/")[0]
print(f"  Target DB: {host}\n")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# ─── SQL Steps ───────────────────────────────────────────────────────────────

STEP_0_PGCRYPTO = "CREATE EXTENSION IF NOT EXISTS pgcrypto;"

STEP_1_BACKFILL_AUTH_USERS = """
INSERT INTO auth.users (
    instance_id,
    id,
    aud,
    role,
    email,
    encrypted_password,
    email_confirmed_at,
    raw_app_meta_data,
    raw_user_meta_data,
    created_at,
    updated_at,
    confirmation_token,
    email_change,
    email_change_token_new,
    recovery_token
)
SELECT
    '00000000-0000-0000-0000-000000000000'::uuid,
    u.id::uuid,
    'authenticated',
    'authenticated',
    u.email,
    COALESCE(u.hashed_password, crypt('TempPassword@123!', gen_salt('bf'))),
    NOW(),
    '{"provider": "email", "providers": ["email"]}'::jsonb,
    jsonb_build_object(
        'name', u.name,
        'role', u.role,
        'department_role', u.department_role
    ),
    COALESCE(u.created_at, NOW()),
    NOW(),
    '', '', '', ''
FROM public.users u
ON CONFLICT (id) DO UPDATE SET
    email                = EXCLUDED.email,
    encrypted_password   = EXCLUDED.encrypted_password,
    raw_user_meta_data   = EXCLUDED.raw_user_meta_data,
    updated_at           = NOW();
"""

STEP_2_BACKFILL_IDENTITIES = """
INSERT INTO auth.identities (
    id,
    user_id,
    provider_id,
    identity_data,
    provider,
    last_sign_in_at,
    created_at,
    updated_at
)
SELECT
    gen_random_uuid(),
    u.id::uuid,
    u.email,
    jsonb_build_object(
        'sub',            u.id::text,
        'email',          u.email,
        'email_verified', true,
        'provider',       'email'
    ),
    'email',
    NOW(),
    NOW(),
    NOW()
FROM public.users u
WHERE NOT EXISTS (
    SELECT 1 FROM auth.identities ai
    WHERE ai.user_id = u.id::uuid
      AND ai.provider = 'email'
);
"""

STEP_3_TRIGGER = """
CREATE OR REPLACE FUNCTION public.handle_new_auth_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER SET search_path = public
AS $$
BEGIN
    INSERT INTO public.users (id, email, name, role, department_role, hashed_password)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'name', split_part(NEW.email, '@', 1)),
        COALESCE(NEW.raw_user_meta_data->>'role', 'employee'),
        NEW.raw_user_meta_data->>'department_role',
        COALESCE(NEW.encrypted_password, 'supabase_managed')
    )
    ON CONFLICT (email) DO UPDATE SET
        id              = EXCLUDED.id,
        name            = COALESCE(EXCLUDED.name, public.users.name),
        role            = COALESCE(EXCLUDED.role, public.users.role),
        department_role = COALESCE(EXCLUDED.department_role, public.users.department_role);
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_auth_user();
"""

STEP_4_RLS = """
ALTER TABLE public.users                  ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.developer_task_states  ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.onboarding_sessions    ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.completed_verify_tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.checklist_items        ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.conversation_logs      ENABLE ROW LEVEL SECURITY;

DO $$
DECLARE
    pol RECORD;
BEGIN
    FOR pol IN
        SELECT policyname, tablename
        FROM pg_policies
        WHERE schemaname = 'public'
          AND tablename IN (
              'users',
              'developer_task_states',
              'onboarding_sessions',
              'completed_verify_tasks',
              'checklist_items',
              'conversation_logs'
          )
    LOOP
        EXECUTE format('DROP POLICY IF EXISTS %I ON public.%I;', pol.policyname, pol.tablename);
    END LOOP;
END;
$$;

-- users: backend full access
CREATE POLICY "service_role_all_users" ON public.users FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "postgres_all_users"     ON public.users FOR ALL TO postgres     USING (true) WITH CHECK (true);
-- users: own row
CREATE POLICY "user_select_own"        ON public.users FOR SELECT TO authenticated USING (auth.uid() = id);
CREATE POLICY "user_update_own"        ON public.users FOR UPDATE TO authenticated USING (auth.uid() = id) WITH CHECK (auth.uid() = id);
-- users: admin all
CREATE POLICY "admin_all_users"        ON public.users FOR ALL TO authenticated
    USING ((auth.jwt() -> 'user_metadata' ->> 'role') = 'admin')
    WITH CHECK ((auth.jwt() -> 'user_metadata' ->> 'role') = 'admin');

-- developer_task_states
CREATE POLICY "service_role_all_dev_tasks" ON public.developer_task_states FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "postgres_all_dev_tasks"     ON public.developer_task_states FOR ALL TO postgres     USING (true) WITH CHECK (true);
CREATE POLICY "user_select_own_dev_tasks"  ON public.developer_task_states FOR SELECT TO authenticated USING (auth.uid() = user_id);
CREATE POLICY "user_update_own_dev_tasks"  ON public.developer_task_states FOR UPDATE TO authenticated USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "admin_all_dev_tasks"        ON public.developer_task_states FOR ALL TO authenticated
    USING ((auth.jwt() -> 'user_metadata' ->> 'role') = 'admin')
    WITH CHECK ((auth.jwt() -> 'user_metadata' ->> 'role') = 'admin');

-- onboarding_sessions
CREATE POLICY "service_role_all_sessions" ON public.onboarding_sessions FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "postgres_all_sessions"     ON public.onboarding_sessions FOR ALL TO postgres     USING (true) WITH CHECK (true);
CREATE POLICY "user_select_own_sessions"  ON public.onboarding_sessions FOR SELECT TO authenticated USING (auth.uid() = user_id);
CREATE POLICY "user_update_own_sessions"  ON public.onboarding_sessions FOR UPDATE TO authenticated USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "admin_all_sessions"        ON public.onboarding_sessions FOR ALL TO authenticated
    USING ((auth.jwt() -> 'user_metadata' ->> 'role') = 'admin')
    WITH CHECK ((auth.jwt() -> 'user_metadata' ->> 'role') = 'admin');

-- completed_verify_tasks
CREATE POLICY "service_role_all_verify" ON public.completed_verify_tasks FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "postgres_all_verify"     ON public.completed_verify_tasks FOR ALL TO postgres     USING (true) WITH CHECK (true);
CREATE POLICY "user_select_own_verify"  ON public.completed_verify_tasks FOR SELECT TO authenticated USING (auth.uid() = user_id);
CREATE POLICY "admin_all_verify"        ON public.completed_verify_tasks FOR ALL TO authenticated
    USING ((auth.jwt() -> 'user_metadata' ->> 'role') = 'admin')
    WITH CHECK ((auth.jwt() -> 'user_metadata' ->> 'role') = 'admin');

-- checklist_items (FK -> onboarding_sessions.id)
CREATE POLICY "service_role_all_checklist" ON public.checklist_items FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "postgres_all_checklist"     ON public.checklist_items FOR ALL TO postgres     USING (true) WITH CHECK (true);
CREATE POLICY "user_select_own_checklist"  ON public.checklist_items FOR SELECT TO authenticated
    USING (EXISTS (SELECT 1 FROM public.onboarding_sessions s WHERE s.id = checklist_items.session_id AND s.user_id = auth.uid()));
CREATE POLICY "user_update_own_checklist"  ON public.checklist_items FOR UPDATE TO authenticated
    USING (EXISTS (SELECT 1 FROM public.onboarding_sessions s WHERE s.id = checklist_items.session_id AND s.user_id = auth.uid()));
CREATE POLICY "admin_all_checklist"        ON public.checklist_items FOR ALL TO authenticated
    USING ((auth.jwt() -> 'user_metadata' ->> 'role') = 'admin')
    WITH CHECK ((auth.jwt() -> 'user_metadata' ->> 'role') = 'admin');

-- conversation_logs (FK -> onboarding_sessions.id)
CREATE POLICY "service_role_all_conv" ON public.conversation_logs FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "postgres_all_conv"     ON public.conversation_logs FOR ALL TO postgres     USING (true) WITH CHECK (true);
CREATE POLICY "user_select_own_conv"  ON public.conversation_logs FOR SELECT TO authenticated
    USING (EXISTS (SELECT 1 FROM public.onboarding_sessions s WHERE s.id = conversation_logs.session_id AND s.user_id = auth.uid()));
CREATE POLICY "admin_all_conv"        ON public.conversation_logs FOR ALL TO authenticated
    USING ((auth.jwt() -> 'user_metadata' ->> 'role') = 'admin')
    WITH CHECK ((auth.jwt() -> 'user_metadata' ->> 'role') = 'admin');
"""

# ─── Verification Queries ──────────────────────────────────────────────────────
VERIFY_AUTH_USERS_COUNT = "SELECT COUNT(*) FROM auth.users;"
VERIFY_IDENTITIES_COUNT = "SELECT COUNT(*) FROM auth.identities WHERE provider = 'email';"
VERIFY_ID_MATCH = """
SELECT u.email, u.id AS public_id, au.id AS auth_id, (u.id = au.id) AS ids_match
FROM public.users u
JOIN auth.users au ON u.email = au.email
ORDER BY u.email;
"""
VERIFY_RLS_POLICIES = """
SELECT tablename, policyname, cmd, roles
FROM pg_policies
WHERE schemaname = 'public'
ORDER BY tablename, policyname;
"""

# ─── Execution ────────────────────────────────────────────────────────────────

def run_step(conn, name: str, sql: str):
    print(f"\n--- {name} ---")
    conn.execute(text(sql))
    print(f"    OK")


def run_migration():
    print("\n[Phase 1: Migration]\n")
    with engine.begin() as conn:
        run_step(conn, "Step 0: Enable pgcrypto extension",             STEP_0_PGCRYPTO)
        run_step(conn, "Step 1: Backfill auth.users from public.users", STEP_1_BACKFILL_AUTH_USERS)
        run_step(conn, "Step 2: Backfill auth.identities",              STEP_2_BACKFILL_IDENTITIES)
        run_step(conn, "Step 3: Create auth -> public sync trigger",    STEP_3_TRIGGER)
        run_step(conn, "Step 4: Enable RLS + create all policies",      STEP_4_RLS)

    print("\n\n[Phase 2: Verification Checkpoints]\n")

    with engine.connect() as conn:
        # Checkpoint 1
        auth_count = conn.execute(text(VERIFY_AUTH_USERS_COUNT)).scalar()
        ok1 = auth_count >= 5 if auth_count else False
        print(f"  [{'PASS' if ok1 else 'FAIL'}] Checkpoint 1 — auth.users count: {auth_count} (expected >= 5)")

        # Checkpoint 2
        identity_count = conn.execute(text(VERIFY_IDENTITIES_COUNT)).scalar()
        ok2 = identity_count >= 5 if identity_count else False
        print(f"  [{'PASS' if ok2 else 'FAIL'}] Checkpoint 2 — auth.identities (email) count: {identity_count} (expected >= 5)")

        # Checkpoint 3
        print(f"\n  [Checkpoint 3 — ID match: public.users <-> auth.users]")
        print(f"  {'Email':<38} {'IDs Match?'}")
        print(f"  {'-'*38} {'-'*10}")
        rows = conn.execute(text(VERIFY_ID_MATCH)).fetchall()
        all_match = all(row[3] for row in rows) if rows else False
        for row in rows:
            print(f"  {row[0]:<38} {'MATCH' if row[3] else 'MISMATCH -- ' + str(row[1]) + ' vs ' + str(row[2])}")
        ok3 = all_match and bool(rows)
        print(f"  [{'PASS' if ok3 else 'FAIL'}] All {len(rows)} users matched with identical IDs")

        # Checkpoint 4
        print(f"\n  [Checkpoint 4 — Active RLS Policies]")
        print(f"  {'Table':<35} {'Policy':<40} {'CMD':<8} Roles")
        print(f"  {'-'*35} {'-'*40} {'-'*8} {'-'*30}")
        policies = conn.execute(text(VERIFY_RLS_POLICIES)).fetchall()
        for p in policies:
            print(f"  {str(p[0]):<35} {str(p[1]):<40} {str(p[2]):<8} {str(p[3])}")
        ok4 = len(policies) > 0
        print(f"  [{'PASS' if ok4 else 'FAIL'}] {len(policies)} RLS policies active")

    print("\n" + "=" * 60)
    overall = all([ok1, ok2, ok3, ok4])
    if overall:
        print("  ALL CHECKPOINTS PASSED — Migration successful!")
    else:
        print("  SOME CHECKPOINTS FAILED — Review output above.")
    print("=" * 60)
    print()
    print("  NEXT STEPS:")
    print("  1. Restart the FastAPI backend:   uvicorn app.main:app --reload")
    print("  2. Try logging in at:             http://localhost:5173")
    print("  3. In Supabase Dashboard -> Authentication > Users")
    print("     You should see all 5 users listed there now.")
    print()

    if not overall:
        sys.exit(1)


if __name__ == "__main__":
    try:
        run_migration()
    except Exception as exc:
        print(f"\nMigration aborted due to error: {exc}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
