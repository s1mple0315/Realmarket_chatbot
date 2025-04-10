import datetime
from pydantic import BaseModel
from bson import ObjectId
from typing import Optional


class BotModel:
    def __init__(
        self,
        name: str,
        description: str,
        model: str,
        user_id: str,
        metadata: dict = None,
        config: dict = None,
    ):
        self.name = name
        self.description = description
        self.model = model
        self.user_id = user_id
        self.metadata = metadata or {}
        self.config = config or {}
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()


class Bot(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    model: str
    user_id: str
    metadata: Optional[dict] = {}
    config: Optional[dict] = {}
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}
