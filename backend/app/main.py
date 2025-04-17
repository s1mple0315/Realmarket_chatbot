from fastapi import FastAPI
from app.api.v1 import router as api_router
from app.middleware import AddUserIDToRequest
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(AddUserIDToRequest)

origins = [
    "http://localhost",
    "http://localhost:4000",
    "http://localhost:4000/",
    "http://localhost:4000/login",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
