# services/assistant_service.py
from app.models.assistant import Assistant, AssistantConfig, AssistantMongoModel
from app.database import db

async def create_assistant(assistant_config: AssistantConfig):
    assistant_data = AssistantMongoModel(
        assistant_config.name,
        assistant_config.instructions,
        assistant_config.tone,
        assistant_config.website_data
    )
    assistant_data.save()
    return Assistant(**assistant_data.__dict__)

async def update_assistant_config(assistant_id: str, new_config: dict):
    AssistantMongoModel.update_assistant(assistant_id, new_config)
    updated_assistant = AssistantMongoModel.get_assistant_by_id(assistant_id)
    return Assistant(**updated_assistant)
