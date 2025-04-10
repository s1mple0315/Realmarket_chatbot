# services/user_service.py
from bson import ObjectId
from app.models.user import User, UserMongoModel
from app.database import db


async def create_user(user: User):
    user_data = UserMongoModel(user.name, user.email)
    user_data.save()
    return user


async def get_user_by_id(user_id: str):
    user = UserMongoModel.get_user_by_id(user_id)
    if user:
        return User(**user)
    return None


async def get_user_by_username(username: str):
    """Fetch a user from the database by their username (email in this case)"""
    users_collection = db.users
    user = users_collection.find_one({"email": username})
    if user:
        return User(**user)
    return None


async def add_assistant_to_user(user_id: str, assistant_id: str):
    user = await get_user_by_id(user_id)
    if user:
        user.assistants.append(assistant_id)
        db.users.update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"assistants": user.assistants}}
        )
