# models/assistant.py
from pydantic import BaseModel
from typing import Optional, Dict
from bson import ObjectId
import datetime
from app.database import db

class AssistantConfig(BaseModel):
    name: str
    instructions: str
    tone: Optional[str] = "neutral"  # E.g., "formal", "casual", etc.
    website_data: Optional[Dict] = {}

class Assistant(BaseModel):
    id: Optional[str] = None
    name: str
    instructions: str
    tone: str
    website_data: dict
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True
        json_encoders = {
            ObjectId: str
        }

class AssistantMongoModel:
    def __init__(self, name: str, instructions: str, tone: str, website_data: dict):
        self.name = name
        self.instructions = instructions
        self.tone = tone
        self.website_data = website_data
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()

    def save(self):
        """Save the assistant to the database."""
        assistants_collection = db.assistants
        assistant_data = self.__dict__
        return assistants_collection.insert_one(assistant_data)
    
    @staticmethod
    def get_assistant_by_id(assistant_id: str):
        """Fetch an assistant by ID."""
        assistants_collection = db.assistants
        return assistants_collection.find_one({"_id": ObjectId(assistant_id)})
    
    @staticmethod
    def update_assistant(assistant_id: str, new_config: dict):
        """Update the assistant's configuration."""
        assistants_collection = db.assistants
        assistants_collection.update_one(
            {"_id": ObjectId(assistant_id)},
            {"$set": new_config}
        )
