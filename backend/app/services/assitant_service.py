# services/assistant_service.py
from app.models.assistant import AssistantConfig
from app.models.assistant import AssistantMongoModel
from app.database import db


async def create_assistant(assistant_config: AssistantConfig):
    """Create and save a new assistant"""
    assistant_data = AssistantMongoModel(
        assistant_config.name,
        assistant_config.instructions,
        assistant_config.tone,
        assistant_config.website_data,
    )
    assistant_data.save()
    return assistant_data


async def update_assistant_config(assistant_id: str, new_config: dict):
    """Update the assistant's configuration in the database"""
    AssistantMongoModel.update_assistant(assistant_id, new_config)
    updated_assistant = AssistantMongoModel.get_assistant_by_id(assistant_id)
    return updated_assistant


async def get_assistant_by_id(assistant_id: str):
    """Fetch an assistant by ID"""
    assistant = AssistantMongoModel.get_assistant_by_id(assistant_id)
    if assistant:
        return assistant
    return None
