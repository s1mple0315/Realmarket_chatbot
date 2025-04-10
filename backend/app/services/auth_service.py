# services/auth_service.py
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from app.services.user_service import get_user_by_username  # Import from user_service
import os
from app.database import db  # Import the database connection
from app.models.user import User, UserMongoModel  # Import the UserMongoModel

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify a password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to create an access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to authenticate user
async def authenticate_user(username: str, password: str) -> Optional[dict]:
    user = await get_user_by_username(username)  # Get user by username (email)
    if not user:
        return None
    if not verify_password(password, user["password"]):
        return None
    return user

# Function to register a user
async def register_user(user: User) -> Optional[dict]:
    # Hash the password before saving the user
    hashed_password = hash_password(user.password)  # Use dot notation to access 'password'
    # Save the user (assumes the existence of UserMongoModel to save to DB)
    user_data = {
        "email": user.email,
        "name": user.name,
        "password": hashed_password,
    }
    user_model = UserMongoModel(**user_data)
    db.users.insert_one(user_model.__dict__)  # Save user data to MongoDB
    return user_data  # Return the newly created user data
