from fastapi import FastAPI
from app.api.v1 import router as api_router
from app.middleware import AddUserIDToRequest

app = FastAPI()

app.add_middleware(AddUserIDToRequest)

app.include_router(api_router, prefix="/api/v1")
