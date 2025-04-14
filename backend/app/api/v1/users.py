# app/api/v1/users.py
from fastapi import APIRouter, HTTPException
from app.models.user import User
from app.services.user_service import create_user, get_user_by_id

router = APIRouter()

@router.post("/users", response_model=User)
async def create_new_user(user: User):
    new_user = await create_user(user)
    return new_user

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
