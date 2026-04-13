import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import asyncio
from app.models.checklist import Base, ChecklistTemplate, ChecklistItem
from app.schemas.persona import DeveloperPersona
from app.services.checklist_service import ChecklistService

# Setup SQLite in-memory DB for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Insert mock templates based on requirements
    templates = [
        ChecklistTemplate(
            item_key="github_access", title="GitHub Access", description="Get access to GitHub repo",
            category="access", required=True, sort_order=1,
            applicable_roles=["all"], applicable_levels=["all"], applicable_stacks=["all"]
        ),
        ChecklistTemplate(
            item_key="local_dev_python", title="Local Dev Python", description="Setup local Python env",
            category="setup", required=True, sort_order=2,
            applicable_roles=["backend", "fullstack", "data"], applicable_levels=["all"], applicable_stacks=["python"]
        ),
        ChecklistTemplate(
            item_key="local_dev_node", title="Local Dev Node", description="Setup local Node env",
            category="setup", required=True, sort_order=3,
            applicable_roles=["frontend", "fullstack"], applicable_levels=["all"], applicable_stacks=["node"]
        ),
        ChecklistTemplate(
            item_key="read_architecture", title="Read Architecture", description="Read the system architecture docs",
            category="documentation", required=True, sort_order=4,
            applicable_roles=["all"], applicable_levels=["mid", "senior"], applicable_stacks=["all"]
        ),
        ChecklistTemplate(
            item_key="read_git_workflow", title="Read Git Workflow", description="Read the git workflow docs",
            category="documentation", required=True, sort_order=5,
            applicable_roles=["all"], applicable_levels=["intern", "junior"], applicable_stacks=["all"]
        ),
        ChecklistTemplate(
            item_key="sign_nda", title="Sign NDA", description="Sign company NDA",
            category="onboarding", required=True, sort_order=6,
            applicable_roles=["all"], applicable_levels=["all"], applicable_stacks=["all"]
        ),
        ChecklistTemplate(
            item_key="docker_setup", title="Docker Setup", description="Setup Docker",
            category="setup", required=True, sort_order=7,
            applicable_roles=["devops", "backend", "fullstack"], applicable_levels=["all"], applicable_stacks=["all"]
        ),
        ChecklistTemplate(
            item_key="ide_setup", title="IDE Setup", description="Setup IDE",
            category="setup", required=False, sort_order=8,
            applicable_roles=["all"], applicable_levels=["all"], applicable_stacks=["all"]
        ),
        # Extra tasks for interns to satisfy AC: "Checklist for intern has more items than for senior"
        ChecklistTemplate(
            item_key="meet_onboarding_buddy", title="Meet your onboarding buddy", description="Have a sync with buddy",
            category="onboarding", required=True, sort_order=9,
            applicable_roles=["all"], applicable_levels=["intern", "junior"], applicable_stacks=["all"]
        ),
        ChecklistTemplate(
            item_key="read_company_history", title="Read company history", description="Learn about the company",
            category="documentation", required=False, sort_order=10,
            applicable_roles=["all"], applicable_levels=["intern"], applicable_stacks=["all"]
        ),
    ]
    db.add_all(templates)
    db.commit()
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def service(db_session):
    return ChecklistService(db=db_session)

@pytest.mark.asyncio
async def test_senior_backend_python(service):
    persona = DeveloperPersona(
        name="Alice",
        email="alice@example.com",
        role="backend",
        experience_level="senior",
        tech_stack=["python", "fastapi", "postgres", "docker"]
    )
    
    items = await service.generate_checklist_for_persona("session-1", persona)
    keys = [item.item_key for item in items]
    
    # Assert they receive specific items
    assert "github_access" in keys
    assert "local_dev_python" in keys
    assert "read_architecture" in keys
    assert "sign_nda" in keys
    assert "docker_setup" in keys
    
    # Assert they do NOT receive local_dev_node or read_git_workflow
    assert "local_dev_node" not in keys
    assert "read_git_workflow" not in keys

@pytest.mark.asyncio
async def test_intern_frontend_node(service):
    persona = DeveloperPersona(
        name="Bob",
        email="bob@example.com",
        role="frontend",
        experience_level="intern",
        tech_stack=["node", "react", "typescript"]
    )
    
    items = await service.generate_checklist_for_persona("session-2", persona)
    keys = [item.item_key for item in items]
    
    # Assert they receive specific items
    assert "github_access" in keys
    assert "local_dev_node" in keys
    assert "read_git_workflow" in keys
    assert "ide_setup" in keys
    
    # Assert they do NOT receive local_dev_python or read_architecture
    assert "local_dev_python" not in keys
    assert "read_architecture" not in keys

@pytest.mark.asyncio
async def test_intern_has_more_items_than_senior(service):
    persona_senior = DeveloperPersona(
        name="Alice", email="a@example.com", role="backend",
        experience_level="senior", tech_stack=["python", "docker"]
    )
    persona_intern = DeveloperPersona(
        name="Bob", email="b@example.com", role="frontend",
        experience_level="intern", tech_stack=["node"]
    )
    
    items_senior = await service.generate_checklist_for_persona("session-senior", persona_senior)
    items_intern = await service.generate_checklist_for_persona("session-intern", persona_intern)
    
    assert len(items_intern) > len(items_senior)

@pytest.mark.asyncio
async def test_get_progress_and_required(service):
    # Test for additional methods to meet AC
    persona = DeveloperPersona(
        name="Charlie", email="c@example.com", role="backend",
        experience_level="senior", tech_stack=["python", "docker"]
    )
    session_id = "prog-test-session"
    items = await service.generate_checklist_for_persona(session_id, persona)
    
    progress = await service.get_progress(session_id)
    assert progress["total_items"] == len(items)
    assert progress["completed"] == 0
    assert progress["pending"] == len(items)
    assert progress["percent_complete"] == 0.0
    
    # all_required_complete should be false initially
    assert not await service.all_required_complete(session_id)
    
    # Update all required items to completed
    required_items = [item for item in items if item.required]
    for item in required_items:
        await service.update_item_status(item.id, "completed")
        
    # Check completed
    assert await service.all_required_complete(session_id)
    
    # Check progress update
    progress = await service.get_progress(session_id)
    assert progress["completed"] == len(required_items)
    assert progress["percent_complete"] > 0
