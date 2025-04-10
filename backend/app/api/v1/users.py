# app/api/v1/users.py
from fastapi import APIRouter, HTTPException
from app.models.user import User
from app.models.assistant import Assistant, AssistantConfig
from app.services.assitant_service import create_assistant
from app.services.user_service import create_user, get_user_by_id, add_assistant_to_user

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

@router.post("/users/{user_id}/assistants", response_model=Assistant)
async def add_assistant_to_user_route(user_id: str, assistant: AssistantConfig):
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_assistant = await create_assistant(assistant)
    await add_assistant_to_user(user_id, new_assistant.id)
    
    return new_assistant
