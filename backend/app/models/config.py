from pydantic import BaseModel
from typing import Optional

class BotConfig(BaseModel):
    tone: Optional[str] = "neutral"  # e.g., "friendly", "formal"
    style: Optional[str] = "casual"  # e.g., "casual", "professional"
    data_collection: Optional[dict] = {}  # E.g., collect email, phone, etc.
    predefined_qna: Optional[dict] = {}  # Predefined questions and answers

    class Config:
        orm_mode = True
