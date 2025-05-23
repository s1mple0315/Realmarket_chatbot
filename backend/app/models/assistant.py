from pydantic import BaseModel
from typing import List, Optional, Dict
from bson import ObjectId
import datetime
from app.database import db


class AssistantConfig(BaseModel):
    name: str
    instructions: str
    description: Optional[str] = None
    tone: Optional[str] = "neutral"
    website_data: Optional[dict] = None
    tools: Optional[List[str]] = []


class Assistant(BaseModel):
    id: Optional[str] = None
    user_id: str
    name: str
    instructions: str
    tone: str
    website_data: dict
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}


class ThreadMongoModel:
    def __init__(self, user_id: str, assistant_id: str, thread_id: str):
        self.user_id = user_id
        self.assistant_id = assistant_id
        self.thread_id = thread_id
        self.created_at = datetime.datetime.utcnow()

    def save(self):
        """Save the thread to the database."""
        threads_collection = db.threads
        thread_data = self.__dict__
        return threads_collection.insert_one(thread_data)


class AssistantMongoModel:
    def __init__(
        self,
        user_id: str,
        assistant_id: str,
        name: str,
        instructions: str,
        tone: str,
        website_data: dict,
    ):
        self.user_id = user_id
        self.assistant_id = assistant_id
        self.name = name
        self.instructions = instructions
        self.tone = tone
        self.website_data = website_data or {}
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()

    def save(self):
        """Save the assistant to the database and return the inserted ID."""
        assistants_collection = db.assistants
        assistant_data = self.__dict__
        result = assistants_collection.insert_one(assistant_data)
        return str(result.inserted_id)

    @staticmethod
    def get_assistant_by_id(assistant_id: str):
        """Fetch an assistant by OpenAI assistant_id."""
        assistants_collection = db.assistants
        return assistants_collection.find_one({"assistant_id": assistant_id})

    @staticmethod
    def update_assistant(assistant_id: str, new_config: dict):
        """Update the assistant's configuration."""
        assistants_collection = db.assistants
        assistants_collection.update_one(
            {"_id": ObjectId(assistant_id)}, {"$set": new_config}
        )
