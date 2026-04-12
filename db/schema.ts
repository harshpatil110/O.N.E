import {
  pgTable,
  uuid,
  varchar,
  text,
  timestamp,
  boolean,
  integer,
  jsonb,
  pgEnum,
} from 'drizzle-orm/pg-core';

export const userRoleEnum = pgEnum('user_role', ['employee', 'hr_admin', 'eng_manager']);
export const sessionStatusEnum = pgEnum('session_status', ['in_progress', 'completed', 'abandoned']);
export const itemCategoryEnum = pgEnum('item_category', ['access', 'tooling', 'documentation', 'compliance', 'team']);
export const itemStatusEnum = pgEnum('item_status', ['pending', 'in_progress', 'completed', 'skipped']);
export const conversationRoleEnum = pgEnum('conversation_role', ['user', 'assistant', 'system']);

export const users = pgTable('users', {
  id: uuid('id').defaultRandom().primaryKey(),
  name: varchar('name', { length: 255 }).notNull(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  role: userRoleEnum('role').default('employee').notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

export const onboardingSessions = pgTable('onboarding_sessions', {
  id: uuid('id').defaultRandom().primaryKey(),
  userId: uuid('user_id')
    .notNull()
    .references(() => users.id, { onDelete: 'cascade' }),
  persona: jsonb('persona'),
  status: sessionStatusEnum('status').default('in_progress').notNull(),
  currentFsmState: varchar('current_fsm_state', { length: 255 }),
  currentChecklistIndex: integer('current_checklist_index').default(0).notNull(),
  startedAt: timestamp('started_at').defaultNow().notNull(),
  completedAt: timestamp('completed_at'),
  hrNotified: boolean('hr_notified').default(false).notNull(),
});

export const checklistItems = pgTable('checklist_items', {
  id: uuid('id').defaultRandom().primaryKey(),
  sessionId: uuid('session_id')
    .notNull()
    .references(() => onboardingSessions.id, { onDelete: 'cascade' }),
  itemKey: varchar('item_key', { length: 255 }).notNull(),
  title: text('title').notNull(),
  description: text('description'),
  category: itemCategoryEnum('category').notNull(),
  required: boolean('required').default(true).notNull(),
  sortOrder: integer('sort_order').notNull(),
  applicableRoles: text('applicable_roles').array(),
  applicableLevels: text('applicable_levels').array(),
  applicableStacks: text('applicable_stacks').array(),
  knowledgeBaseRefs: text('knowledge_base_refs').array(),
  status: itemStatusEnum('status').default('pending').notNull(),
  completedAt: timestamp('completed_at'),
});

export const conversationLogs = pgTable('conversation_logs', {
  id: uuid('id').defaultRandom().primaryKey(),
  sessionId: uuid('session_id')
    .notNull()
    .references(() => onboardingSessions.id, { onDelete: 'cascade' }),
  role: conversationRoleEnum('role').notNull(),
  content: text('content').notNull(),
  metadata: jsonb('metadata'),
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

export const checklistTemplates = pgTable('checklist_templates', {
  id: uuid('id').defaultRandom().primaryKey(),
  itemKey: varchar('item_key', { length: 255 }).notNull().unique(),
  title: text('title').notNull(),
  description: text('description'),
  category: itemCategoryEnum('category').notNull(),
  required: boolean('required').default(true).notNull(),
  sortOrder: integer('sort_order').notNull(),
  applicableRoles: text('applicable_roles').array(),
  applicableLevels: text('applicable_levels').array(),
  applicableStacks: text('applicable_stacks').array(),
  knowledgeBaseRefs: text('knowledge_base_refs').array(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
});
