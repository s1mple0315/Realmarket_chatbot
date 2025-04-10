# models/user.py
from pydantic import BaseModel, EmailStr
from bson import ObjectId
from typing import List, Optional
import datetime

# MongoDB Model for User
class UserMongoModel:
    def __init__(
        self, name: str, email: EmailStr, password: str, assistants: Optional[List[str]] = None
    ):
        self.name = name
        self.email = email
        self.password = password  # Store password (hashed in registration process)
        self.assistants = assistants or []
        self.created_at = datetime.datetime.utcnow()

    def save(self):
        """Save the user to the database."""
        users_collection = db.users
        user_data = self.__dict__
        return users_collection.insert_one(user_data)

    @staticmethod
    def get_user_by_id(user_id: str):
        """Fetch a user by ID."""
        users_collection = db.users
        return users_collection.find_one({"_id": ObjectId(user_id)})

class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    password: Optional[str] = None 
    assistants: List[str] = []
    created_at: datetime.datetime

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}
        # Exclude password from responses
        fields = {'password': {'exclude': True}}

