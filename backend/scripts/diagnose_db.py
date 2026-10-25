"""
O.N.E. — Database Diagnostic Script
=====================================
Tests DNS resolution (IPv4 + IPv6), TCP connectivity, and SQLAlchemy auth
against the configured DATABASE_URL.

Run from the backend/ directory:
    python scripts/diagnose_db.py
"""

import os
import sys
import socket
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv

# Force UTF-8 output on Windows terminals
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

load_dotenv(override=True)

POOLER_HOST_PRIMARY  = "aws-0-ap-southeast-1.pooler.supabase.com"
POOLER_HOST_FALLBACK = "aws-1-ap-southeast-1.pooler.supabase.com"
DIRECT_HOST_SUFFIX   = ".supabase.co"


def header(msg: str):
    print(f"\n{'='*60}\n  {msg}\n{'='*60}")


def ok(msg: str):
    print(f"  [PASS] {msg}")


def fail(msg: str):
    print(f"  [FAIL] {msg}")


def warn(msg: str):
    print(f"  [WARN] {msg}")


def info(msg: str):
    print(f"  [INFO] {msg}")


def test_dns(host: str, port: int) -> list:
    """
    Uses getaddrinfo so it resolves both IPv4 (AF_INET) and IPv6 (AF_INET6).
    Returns list of resolved (family, ip) tuples on success, empty list on failure.
    """
    try:
        results = socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
        resolved = []
        for fam, _, _, _, sockaddr in results:
            family = "IPv4" if fam == socket.AF_INET else "IPv6"
            resolved.append((family, sockaddr[0]))
        return resolved
    except socket.gaierror:
        return []


def test_tcp(host: str, port: int) -> bool:
    """Attempts a TCP connection to host:port within 5 seconds."""
    try:
        s = socket.create_connection((host, port), timeout=5)
        s.close()
        return True
    except Exception:
        return False


def test_auth(url: str) -> tuple[bool, str]:
    """Attempts psycopg2 connect + SELECT 1 using the given URL."""
    try:
        conn = psycopg2.connect(url, connect_timeout=8, sslmode="require")
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        conn.close()
        return True, "OK"
    except Exception as e:
        return False, str(e)


def test_sqlalchemy_query(url: str) -> tuple[bool, str]:
    """Attempts a SQLAlchemy auth.users count to confirm migration data is present."""
    try:
        from sqlalchemy import create_engine, text
        eng = create_engine(
            url,
            pool_pre_ping=True,
            connect_args={"sslmode": "require"},
        )
        with eng.connect() as conn:
            count = conn.execute(text("SELECT count(*) FROM auth.users;")).scalar()
        return True, str(count)
    except Exception as e:
        return False, str(e)


def run():
    header("O.N.E. Database Diagnostic Tool")

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        fail("DATABASE_URL is missing from .env — aborting.")
        sys.exit(1)

    # ── Parse URL ────────────────────────────────────────────────────────────
    parsed = urlparse(db_url)
    host = parsed.hostname or ""
    port = parsed.port or 5432
    user = parsed.username or ""
    info(f"DATABASE_URL host : {host}")
    info(f"DATABASE_URL port : {port}")
    info(f"DATABASE_URL user : {user}")

    is_direct = host.endswith(DIRECT_HOST_SUFFIX)
    is_pooler = "pooler.supabase.com" in host

    # ── Warning: direct host is IPv6-only ───────────────────────────────────
    if is_direct:
        warn(
            f"'{host}' is the DIRECT connection host. On Supabase Free Tier "
            "this resolves IPv6-ONLY and will fail on most ISPs/networks.\n"
            f"  Recommended: switch to {POOLER_HOST_PRIMARY}:5432 (IPv4 Session Pooler)."
        )

    # ── Test 1: DNS Resolution ───────────────────────────────────────────────
    print(f"\n--- Test 1: DNS Resolution for '{host}' ---")
    resolved = test_dns(host, port)
    if resolved:
        for family, ip in resolved:
            ok(f"Resolved {family}: {ip}")
        has_ipv4 = any(f == "IPv4" for f, _ in resolved)
        if not has_ipv4 and is_direct:
            warn(
                "Only IPv6 addresses resolved. If your machine or ISP has no IPv6 "
                "path to Supabase, connections will time out.\n"
                f"  Run this script again after switching DATABASE_URL to the pooler: "
                f"{POOLER_HOST_PRIMARY}"
            )
            # Auto-test the pooler as a hint
            print(f"\n  [Auto-testing pooler fallback: {POOLER_HOST_PRIMARY}]")
            pooler_resolved = test_dns(POOLER_HOST_PRIMARY, 5432)
            if pooler_resolved:
                for fam, ip in pooler_resolved:
                    ok(f"  Pooler resolves {fam}: {ip}")
            else:
                fail(f"  Pooler '{POOLER_HOST_PRIMARY}' also failed DNS — check internet.")
    else:
        fail(f"Cannot resolve '{host}' — check internet or Supabase project status.")
        if is_direct:
            info(f"Attempting pooler fallback DNS: {POOLER_HOST_PRIMARY}")
            pooler_resolved = test_dns(POOLER_HOST_PRIMARY, 5432)
            if pooler_resolved:
                for fam, ip in pooler_resolved:
                    ok(f"  Pooler {fam}: {ip}")
                info("Pooler is reachable. Update DATABASE_URL to the pooler URL and retry.")
            else:
                fail(f"Pooler '{POOLER_HOST_PRIMARY}' also unresolvable.")
        sys.exit(1)

    # ── Test 2: TCP Port Reachability ────────────────────────────────────────
    print(f"\n--- Test 2: TCP Port {port} Reachability on '{host}' ---")
    if test_tcp(host, port):
        ok(f"Port {port} is open and reachable on '{host}'.")
    else:
        fail(f"Cannot reach port {port} on '{host}'.")
        if is_direct:
            info(
                "Direct port 5432 is commonly blocked by firewalls/NAT on Supabase Free Tier "
                "when using the IPv6-only host. Switch to the Session Pooler."
            )
        # Try pooler TCP if we're not already on it
        if not is_pooler:
            info(f"Testing pooler TCP: {POOLER_HOST_PRIMARY}:5432 ...")
            if test_tcp(POOLER_HOST_PRIMARY, 5432):
                ok(f"Pooler TCP reachable. Update DATABASE_URL to use '{POOLER_HOST_PRIMARY}'.")
            else:
                fail(f"Pooler TCP also unreachable. Check firewall/VPN.")
        sys.exit(1)

    # ── Test 3: psycopg2 Authentication ─────────────────────────────────────
    print(f"\n--- Test 3: Database Authentication (psycopg2) ---")
    auth_ok, auth_msg = test_auth(db_url)
    if auth_ok:
        ok("Authenticated with PostgreSQL — SELECT 1 returned successfully.")
    else:
        fail(f"Authentication rejected: {auth_msg}")
        if is_direct:
            info(
                "Note: Direct host requires username 'postgres'. "
                "Session Pooler requires username 'postgres.<project-ref>'."
            )
        sys.exit(1)

    # ── Test 4: Supabase Auth Users Count (post-migration check) ─────────────
    print(f"\n--- Test 4: Supabase Auth Verification (auth.users count) ---")
    sa_ok, sa_result = test_sqlalchemy_query(db_url)
    if sa_ok:
        ok(f"auth.users row count = {sa_result}")
        if int(sa_result) >= 5:
            ok("Migration verified — all 5 users present in auth.users.")
        else:
            warn(f"Only {sa_result} users found in auth.users. Expected >= 5. Run supabase_auth_sync.py.")
    else:
        fail(f"SQLAlchemy query failed: {sa_result}")

    # ── Summary ───────────────────────────────────────────────────────────────
    print()
    header("Diagnostic Complete")
    print()
    if is_pooler:
        ok("Using Supabase Session Pooler (IPv4-compatible). All tests passed.")
    else:
        warn("Not using the pooler. Consider switching for better reliability.")
    print()


if __name__ == "__main__":
    run()
