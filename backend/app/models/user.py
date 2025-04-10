import datetime
from pydantic import BaseModel, EmailStr
from bson import ObjectId
from typing import Optional


class UserModel:
    def __init__(
        self,
        name: str,
        surname: str,
        email: EmailStr,
        phone_number: Optional[str] = None,
        role: str = "user",
    ):
        self.name = name
        self.surname = surname
        self.email = email
        self.phone_number = phone_number
        self.role = role
        self.created_at = datetime.datetime.utcnow()


class User(BaseModel):
    id: Optional[str] = None
    name: str
    surname: str
    email: EmailStr
    phone_number: Optional[str] = None
    role: str = "user"
    created_at: datetime.datetime

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}
