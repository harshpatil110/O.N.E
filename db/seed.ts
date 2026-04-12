import { neon } from '@neondatabase/serverless';
import { drizzle } from 'drizzle-orm/neon-http';
import { checklistTemplates } from './schema';

// This is necessary if running directly via something like tsx without pre-loading env vars
import * as dotenv from 'dotenv';
dotenv.config();

if (!process.env.DATABASE_URL) {
  throw new Error('DATABASE_URL is missing in the environment');
}

const sql = neon(process.env.DATABASE_URL);
const db = drizzle(sql);

const seedData = [
  {
    itemKey: 'github_access',
    title: 'GitHub org access and repo permissions',
    category: 'access' as const,
    required: true,
    sortOrder: 10,
    applicableRoles: ['all'],
    applicableLevels: ['all'],
    applicableStacks: ['all'],
  },
  {
    itemKey: 'jira_access',
    title: 'Jira project board access',
    category: 'access' as const,
    required: true,
    sortOrder: 20,
    applicableRoles: ['all'],
    applicableLevels: ['all'],
    applicableStacks: ['all'],
  },
  {
    itemKey: 'slack_access',
    title: 'Join Slack channels: #engineering, #backend, #incidents',
    category: 'access' as const,
    required: true,
    sortOrder: 30,
    applicableRoles: ['all'],
    applicableLevels: ['all'],
    applicableStacks: ['all'],
  },
  {
    itemKey: 'local_dev_python',
    title: 'Local dev environment setup (Python 3.11, Poetry, Docker)',
    category: 'tooling' as const,
    required: true,
    sortOrder: 40,
    applicableRoles: ['backend', 'fullstack', 'data'],
    applicableLevels: ['all'],
    applicableStacks: ['python', 'backend'],
  },
  {
    itemKey: 'local_dev_node',
    title: 'Local dev environment setup (Node 20, npm, nvm)',
    category: 'tooling' as const,
    required: true,
    sortOrder: 50,
    applicableRoles: ['frontend', 'fullstack'],
    applicableLevels: ['all'],
    applicableStacks: ['node', 'frontend'],
  },
  {
    itemKey: 'ide_setup',
    title: 'IDE setup with linting and formatting configs',
    category: 'tooling' as const,
    required: false,
    sortOrder: 60,
    applicableRoles: ['all'],
    applicableLevels: ['all'],
    applicableStacks: ['all'],
  },
  {
    itemKey: 'read_architecture',
    title: 'Read Architecture Decision Records (ADRs)',
    category: 'documentation' as const,
    required: true,
    sortOrder: 70,
    applicableRoles: ['all'],
    applicableLevels: ['mid', 'senior', 'staff'],
    applicableStacks: ['all'],
  },
  {
    itemKey: 'read_api_guidelines',
    title: 'Review API design guidelines',
    category: 'documentation' as const,
    required: true,
    sortOrder: 80,
    applicableRoles: ['backend', 'fullstack'],
    applicableLevels: ['all'],
    applicableStacks: ['all'],
  },
  {
    itemKey: 'read_deployment_runbook',
    title: 'Review deployment runbook',
    category: 'documentation' as const,
    required: true,
    sortOrder: 90,
    applicableRoles: ['backend', 'devops', 'fullstack'],
    applicableLevels: ['all'],
    applicableStacks: ['all'],
  },
  {
    itemKey: 'read_git_workflow',
    title: 'Read intro to Git workflow and branching conventions',
    category: 'documentation' as const,
    required: true,
    sortOrder: 100,
    applicableRoles: ['all'],
    applicableLevels: ['intern', 'junior'],
    applicableStacks: ['all'],
  },
  {
    itemKey: 'read_coding_standards',
    title: 'Review coding standards and code review process',
    category: 'documentation' as const,
    required: true,
    sortOrder: 110,
    applicableRoles: ['all'],
    applicableLevels: ['all'],
    applicableStacks: ['all'],
  },
  {
    itemKey: 'sign_nda',
    title: 'Sign NDA and IP agreement',
    category: 'compliance' as const,
    required: true,
    sortOrder: 120,
    applicableRoles: ['all'],
    applicableLevels: ['all'],
    applicableStacks: ['all'],
  },
  {
    itemKey: 'security_training',
    title: 'Complete security awareness training',
    category: 'compliance' as const,
    required: true,
    sortOrder: 130,
    applicableRoles: ['all'],
    applicableLevels: ['all'],
    applicableStacks: ['all'],
  },
  {
    itemKey: 'meet_manager',
    title: 'Schedule 1:1 with engineering manager',
    category: 'team' as const,
    required: true,
    sortOrder: 140,
    applicableRoles: ['all'],
    applicableLevels: ['all'],
    applicableStacks: ['all'],
  },
  {
    itemKey: 'buddy_session',
    title: 'Schedule buddy pairing session',
    category: 'team' as const,
    required: true,
    sortOrder: 150,
    applicableRoles: ['all'],
    applicableLevels: ['all'],
    applicableStacks: ['all'],
  },
  {
    itemKey: 'cicd_setup',
    title: 'Review CI/CD pipeline documentation',
    category: 'documentation' as const,
    required: true,
    sortOrder: 160,
    applicableRoles: ['devops', 'backend'],
    applicableLevels: ['all'],
    applicableStacks: ['all'],
  },
  {
    itemKey: 'docker_setup',
    title: 'Docker installation and local container setup',
    category: 'tooling' as const,
    required: true,
    sortOrder: 170,
    applicableRoles: ['devops', 'backend', 'fullstack'],
    applicableLevels: ['all'],
    applicableStacks: ['all'],
  },
  {
    itemKey: 'python_venv',
    title: 'Set up Python virtual environment using Poetry',
    category: 'tooling' as const,
    required: true,
    sortOrder: 180,
    applicableRoles: ['backend', 'data', 'fullstack'],
    applicableLevels: ['all'],
    applicableStacks: ['python'],
  },
  {
    itemKey: 'read_org_structure',
    title: 'Read org structure and team communication guidelines',
    category: 'documentation' as const,
    required: false,
    sortOrder: 190,
    applicableRoles: ['all'],
    applicableLevels: ['intern', 'junior'],
    applicableStacks: ['all'],
  },
  {
    itemKey: 'first_commit',
    title: 'Create a test branch and make a conventional commit',
    category: 'tooling' as const,
    required: true,
    sortOrder: 200,
    applicableRoles: ['all'],
    applicableLevels: ['intern', 'junior'],
    applicableStacks: ['all'],
  },
  {
    itemKey: 'database_access',
    title: 'Request read-only database access via teleport',
    category: 'access' as const,
    required: true,
    sortOrder: 210,
    applicableRoles: ['backend', 'data', 'fullstack'],
    applicableLevels: ['mid', 'senior'],
    applicableStacks: ['all'],
  }
];

async function main() {
  console.log('Starting checklist templates seed...');

  try {
    for (const item of seedData) {
      await db.insert(checklistTemplates)
        .values(item)
        .onConflictDoNothing({ target: checklistTemplates.itemKey });
    }
    console.log('Successfully seeded checklist templates.');
    process.exit(0);
  } catch (error) {
    console.error('Error seeding checklist templates:', error);
    process.exit(1);
  }
}

main();
