CREATE TYPE "public"."conversation_role" AS ENUM('user', 'assistant', 'system');--> statement-breakpoint
CREATE TYPE "public"."item_category" AS ENUM('access', 'tooling', 'documentation', 'compliance', 'team');--> statement-breakpoint
CREATE TYPE "public"."item_status" AS ENUM('pending', 'in_progress', 'completed', 'skipped');--> statement-breakpoint
CREATE TYPE "public"."session_status" AS ENUM('in_progress', 'completed', 'abandoned');--> statement-breakpoint
CREATE TYPE "public"."user_role" AS ENUM('employee', 'hr_admin', 'eng_manager');--> statement-breakpoint
CREATE TABLE "checklist_items" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"session_id" uuid NOT NULL,
	"item_key" varchar(255) NOT NULL,
	"title" text NOT NULL,
	"description" text,
	"category" "item_category" NOT NULL,
	"required" boolean DEFAULT true NOT NULL,
	"sort_order" integer NOT NULL,
	"applicable_roles" text[],
	"applicable_levels" text[],
	"applicable_stacks" text[],
	"knowledge_base_refs" text[],
	"status" "item_status" DEFAULT 'pending' NOT NULL,
	"completed_at" timestamp
);
--> statement-breakpoint
CREATE TABLE "checklist_templates" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"item_key" varchar(255) NOT NULL,
	"title" text NOT NULL,
	"description" text,
	"category" "item_category" NOT NULL,
	"required" boolean DEFAULT true NOT NULL,
	"sort_order" integer NOT NULL,
	"applicable_roles" text[],
	"applicable_levels" text[],
	"applicable_stacks" text[],
	"knowledge_base_refs" text[],
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "checklist_templates_item_key_unique" UNIQUE("item_key")
);
--> statement-breakpoint
CREATE TABLE "conversation_logs" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"session_id" uuid NOT NULL,
	"role" "conversation_role" NOT NULL,
	"content" text NOT NULL,
	"metadata" jsonb,
	"created_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "onboarding_sessions" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"user_id" uuid NOT NULL,
	"persona" jsonb,
	"status" "session_status" DEFAULT 'in_progress' NOT NULL,
	"current_fsm_state" varchar(255),
	"current_checklist_index" integer DEFAULT 0 NOT NULL,
	"started_at" timestamp DEFAULT now() NOT NULL,
	"completed_at" timestamp,
	"hr_notified" boolean DEFAULT false NOT NULL
);
--> statement-breakpoint
CREATE TABLE "users" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"name" varchar(255) NOT NULL,
	"email" varchar(255) NOT NULL,
	"role" "user_role" DEFAULT 'employee' NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "users_email_unique" UNIQUE("email")
);
--> statement-breakpoint
ALTER TABLE "checklist_items" ADD CONSTRAINT "checklist_items_session_id_onboarding_sessions_id_fk" FOREIGN KEY ("session_id") REFERENCES "public"."onboarding_sessions"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "conversation_logs" ADD CONSTRAINT "conversation_logs_session_id_onboarding_sessions_id_fk" FOREIGN KEY ("session_id") REFERENCES "public"."onboarding_sessions"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "onboarding_sessions" ADD CONSTRAINT "onboarding_sessions_user_id_users_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE cascade ON UPDATE no action;