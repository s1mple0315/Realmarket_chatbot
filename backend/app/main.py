from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import router as api_router
from app.config import redis_client
from loguru import logger
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

app = FastAPI()


class AddUserIDToRequest:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        scope["state"] = scope.get("state", {})
        scope["state"]["user_id"] = "anonymous"
        await self.app(scope, receive, send)


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


@app.on_event("startup")
async def startup():
    logger.info("Starting FastAPI application")
    try:
        await FastAPILimiter.init(redis_client)
        logger.info("FastAPILimiter initialized")
    except Exception as e:
        logger.error(f"Failed to initialize FastAPILimiter: {str(e)}")
        raise

    from app.database import db

    try:
        db.threads.create_index("created_at", expireAfterSeconds=604800)  # 7 days
        logger.info("Created TTL index for threads")
    except Exception as e:
        logger.error(f"Failed to create TTL index: {str(e)}")
        raise


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


app.include_router(api_router, prefix="/api/v1")
