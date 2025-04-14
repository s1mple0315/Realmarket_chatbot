# api/v1/assistants.py
from fastapi import APIRouter, HTTPException, Depends
from app.dependencies import get_user_id_from_token
from app.models.assistant import Assistant, AssistantConfig
from app.services.assitant_service import create_assistant, get_assistant_by_id, update_assistant_config

router = APIRouter()

# Create a new assistant for a user
@router.post("/", response_model=Assistant)
async def create_new_assistant(assistant_config: AssistantConfig, user_id: str = Depends(get_user_id_from_token)):
    new_assistant = await create_assistant(assistant_config, user_id)
    return new_assistant

# Update an assistant's configuration
@router.put("/{assistant_id}", response_model=Assistant)
async def update_assistant(assistant_id: str, assistant_config: AssistantConfig):
    updated_assistant = await update_assistant_config(assistant_id, assistant_config.dict())
    if not updated_assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")
    return updated_assistant

# Get an assistant by ID
@router.get("/{assistant_id}", response_model=Assistant)
async def get_assistant(assistant_id: str):
    assistant = await get_assistant_by_id(assistant_id)
    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")
    return assistant
