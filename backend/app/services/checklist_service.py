from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import asc
from app.schemas.persona import DeveloperPersona
from app.models.checklist import ChecklistTemplate, ChecklistItem

class ChecklistService:
    def __init__(self, db: Session):
        self.db = db

    async def generate_checklist_for_persona(
        self, session_id: str, persona: DeveloperPersona
    ) -> List[ChecklistItem]:
        """
        Algorithm:
        1. Load ALL items from checklist_template table
        2. Filter: keep item if persona.role in item.applicable_roles OR "all" in item.applicable_roles
        3. Filter: keep item if persona.experience_level in item.applicable_levels OR "all" in item.applicable_levels
        4. Filter: keep item if any tech in persona.tech_stack is in item.applicable_stacks OR "all" in item.applicable_stacks
        5. Sort by item.sort_order
        6. Create ChecklistItem rows in DB for this session_id
        7. Return list of created ChecklistItem objects
        """
        templates = self.db.query(ChecklistTemplate).all()
        
        filtered_items = []
        for item in templates:
            role_match = "all" in item.applicable_roles or persona.role in item.applicable_roles
            level_match = "all" in item.applicable_levels or persona.experience_level in item.applicable_levels
            
            # Using any() to check if there is an intersection between the two lists
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
            
        return created_items

    async def get_checklist(self, session_id: str) -> List[ChecklistItem]:
        return self.db.query(ChecklistItem)\
            .filter(ChecklistItem.session_id == session_id)\
            .order_by(asc(ChecklistItem.sort_order))\
            .all()

    async def get_current_item(self, session_id: str) -> Optional[ChecklistItem]:
        return self.db.query(ChecklistItem)\
            .filter(ChecklistItem.session_id == session_id)\
            .filter(ChecklistItem.status.in_(["pending", "in_progress"]))\
            .order_by(asc(ChecklistItem.sort_order))\
            .first()

    async def update_item_status(
        self, item_id: str, status: str, notes: Optional[str] = None
    ) -> Optional[ChecklistItem]:
        # Handle string or int conversion for ID based on the DB schema
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
        return item

    async def get_progress(self, session_id: str) -> dict:
        items = self.db.query(ChecklistItem).filter(ChecklistItem.session_id == session_id).all()
        total_items = len(items)
        
        completed = sum(1 for item in items if item.status == "completed")
        pending = sum(1 for item in items if item.status in ["pending", "in_progress"])
        skipped = sum(1 for item in items if item.status == "skipped")
        
        percent_complete = (completed / total_items * 100) if total_items > 0 else 0.0
        
        return {
            "total_items": total_items,
            "completed": completed,
            "pending": pending,
            "skipped": skipped,
            "percent_complete": round(percent_complete, 2)
        }

    async def all_required_complete(self, session_id: str) -> bool:
        required_items = self.db.query(ChecklistItem)\
            .filter(ChecklistItem.session_id == session_id)\
            .filter(ChecklistItem.required == True)\
            .all()
            
        if not required_items:
            return True
            
        return all(item.status == "completed" for item in required_items)
