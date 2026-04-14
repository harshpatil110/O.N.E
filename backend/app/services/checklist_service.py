import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import asc
from app.schemas.persona import DeveloperPersona
from app.models.checklist_item import ChecklistItem
from app.models.checklist_template import ChecklistTemplate

logger = logging.getLogger(__name__)

class ChecklistService:
    """
    Manages the lifecycle of the onboarding checklist, including generation, 
    retrieval, and status updates of checklist items.
    """
    def __init__(self, db: Session):
        """
        Initializes the service with a database session.
        """
        self.db = db

    async def generate_checklist_for_persona(
        self, session_id: str, persona: DeveloperPersona
    ) -> List[ChecklistItem]:
        """
        Generates a tailored onboarding checklist based on the user's persona.

        Args:
            session_id (str): The ID of the onboarding session.
            persona (DeveloperPersona): The detected developer persona (role, level, tech stack).

        Returns:
            List[ChecklistItem]: The list of newly created checklist items.
        """
        templates = self.db.query(ChecklistTemplate).all()
        
        filtered_items = []
        for item in templates:
            role_match = "all" in item.applicable_roles or persona.role in item.applicable_roles
            level_match = "all" in item.applicable_levels or persona.experience_level in item.applicable_levels
            
            # Intersection between persona tech stack and template stacks
            stack_match = "all" in item.applicable_stacks or any(tech in item.applicable_stacks for tech in persona.tech_stack)
            
            if role_match and level_match and stack_match:
                filtered_items.append(item)
                
        # Sort by sort_order
        filtered_items.sort(key=lambda x: x.sort_order if x.sort_order is not None else 0)
        
        created_items = []
        for idx, template_item in enumerate(filtered_items):
            checklist_item = ChecklistItem(
                session_id=session_id,
                item_key=template_item.item_key,
                title=template_item.title,
                description=template_item.description,
                category=template_item.category,
                required=template_item.required,
                sort_order=idx,
                applicable_roles=template_item.applicable_roles,
                applicable_levels=template_item.applicable_levels,
                applicable_stacks=template_item.applicable_stacks,
                knowledge_base_refs=template_item.knowledge_base_refs,
                status="pending"
            )
            self.db.add(checklist_item)
            created_items.append(checklist_item)
            
        self.db.commit()
        for item in created_items:
            self.db.refresh(item)
            
        logger.info(f"Generated {len(created_items)} checklist items for session {session_id}")
        return created_items

    async def get_checklist(self, session_id: str) -> List[ChecklistItem]:
        """Returns the complete list of checklist items for a session."""
        return self.db.query(ChecklistItem)\
            .filter(ChecklistItem.session_id == session_id)\
            .order_by(asc(ChecklistItem.sort_order))\
            .all()

    async def get_current_item(self, session_id: str) -> Optional[ChecklistItem]:
        """Returns the first pending or in-progress checklist item based on sort order."""
        return self.db.query(ChecklistItem)\
            .filter(ChecklistItem.session_id == session_id)\
            .filter(ChecklistItem.status.in_(["pending", "in_progress"]))\
            .order_by(asc(ChecklistItem.sort_order))\
            .first()

    async def update_item_status(
        self, item_id: str, status: str, notes: Optional[str] = None
    ) -> Optional[ChecklistItem]:
        """
        Updates the status of a specific checklist item.

        Args:
            item_id (str): The ID of the item.
            status (str): New status (e.g. 'completed', 'skipped', 'in_progress').
            notes (str, optional): Additional context or documentation links.

        Returns:
            ChecklistItem, optional: The updated item if found.
        """
        try:
            item = self.db.query(ChecklistItem).filter(ChecklistItem.id == int(item_id)).first()
            if not item:
                return None
                
            item.status = status
            if notes is not None:
                item.notes = notes
                
            if status == "completed":
                item.completed_at = datetime.now(timezone.utc)
                
            self.db.commit()
            self.db.refresh(item)
            logger.info(f"Updated item {item_id} to status: {status}")
            return item
        except Exception as e:
            logger.error(f"Failed to update checklist item {item_id}: {str(e)}")
            return None

    async def get_progress(self, session_id: str) -> dict:
        """
        Calculates the onboarding progress metrics for a session.

        Returns:
            dict: Summary metrics including total items, completion counts, and percentage.
        """
        items = await self.get_checklist(session_id)
        total_items = len(items)
        
        completed_count = sum(1 for item in items if item.status == "completed")
        pending = sum(1 for item in items if item.status in ["pending", "in_progress"])
        skipped = sum(1 for item in items if item.status == "skipped")
        
        percent_complete = (completed_count / total_items * 100) if total_items > 0 else 0.0
        
        return {
            "total_items": total_items,
            "completed_count": completed_count,
            "pending": pending,
            "skipped": skipped,
            "percent_complete": round(percent_complete, 2),
            "items": items
        }

    async def all_required_complete(self, session_id: str) -> bool:
        """Checks if all required onboarding items are marked as completed."""
        required_items = self.db.query(ChecklistItem)\
            .filter(ChecklistItem.session_id == session_id)\
            .filter(ChecklistItem.required == True)\
            .all()
            
        if not required_items:
            return True
            
        return all(item.status == "completed" for item in required_items)
