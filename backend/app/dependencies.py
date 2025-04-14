from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt
from app.services.auth_service import SECRET_KEY, ALGORITHM
from app.models.user import User
from datetime import datetime, timedelta

def get_user_id_from_token(request: Request):
    token = request.headers.get("Authorization")
    if token is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    try:
        token = token.split("Bearer ")[1]  # Extract token from 'Bearer <token>'
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token does not have user_id")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
