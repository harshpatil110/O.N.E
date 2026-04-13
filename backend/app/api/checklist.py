from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth_deps import get_current_user
from app.services.checklist_service import ChecklistService
from app.schemas.checklist import UpdateChecklistRequest
from app.schemas.auth import UserResponse

router = APIRouter()

@router.patch("/checklist/{item_id}")
async def update_item_status(
    item_id: str,
    request: UpdateChecklistRequest,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Update the status (and potentially notes) of a checklist item.
    """
    checklist_service = ChecklistService(db)
    
    # Ideally, we should verify the `current_user` actually owns the session this checklist item
    # belongs to. This implementation delegates to the service for the raw update.
    
    updated_item = await checklist_service.update_item_status(
        item_id=item_id, 
        status=request.status, 
        notes=request.notes
    )
    
    if not updated_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Checklist item not found"
        )
        
    return updated_item
