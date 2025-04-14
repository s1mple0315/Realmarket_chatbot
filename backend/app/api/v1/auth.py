# api/v1/auth.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import authenticate_user, create_access_token, register_user
from app.models.user import User

router = APIRouter()

# Register new user
@router.post("/register", response_model=User)
async def register_user_route(user: User):
    new_user = await register_user(user)
    if not new_user:
        raise HTTPException(status_code=400, detail="User registration failed")
    return new_user  # This will return user data without the password

# Login user and return JWT token
@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}
