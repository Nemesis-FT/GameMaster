from typing import Optional

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from backend.crud import quick_retrieve
from backend.database.models import User
from backend.dependencies import dep_dbsession
from backend.schemas import full
from backend.authentication import get_current_user

router = APIRouter(
    prefix="/api/v1/users",
    tags=["courses"],
    responses={404: {"description": "Not found"}}
)


@router.get("/me", response_model=full.UserFull)
async def user_me(current_user_id=Depends(get_current_user), db: Session = Depends(dep_dbsession)):
    return quick_retrieve(db, User, id=current_user_id)
