# services/assistant_service.py
from app.models.assistant import AssistantConfig
from app.models.assistant import AssistantMongoModel
from app.database import db

async def create_assistant(assistant_config: AssistantConfig, user_id: str):
    """Create and save a new assistant linked to a user"""
    assistant_data = AssistantMongoModel(
        user_id=user_id,  # Associate the assistant with the user
        name=assistant_config.name,
        instructions=assistant_config.instructions,
        tone=assistant_config.tone,
        website_data=assistant_config.website_data
    )
    assistant_data.save()
    return assistant_data  # Return the assistant data after saving it

async def update_assistant_config(assistant_id: str, new_config: dict):
    """Update the assistant's configuration in the database"""
    AssistantMongoModel.update_assistant(assistant_id, new_config)
    updated_assistant = AssistantMongoModel.get_assistant_by_id(assistant_id)
    return updated_assistant  # Return the updated assistant data

async def get_assistant_by_id(assistant_id: str):
    """Fetch an assistant by ID"""
    assistant = AssistantMongoModel.get_assistant_by_id(assistant_id)
    if assistant:
        return assistant
    return None
