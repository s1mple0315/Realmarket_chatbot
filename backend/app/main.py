from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.api.v1 import router as api_router
from app.config import redis_client
from loguru import logger
from pathlib import Path
from fastapi.staticfiles import StaticFiles
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


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="RealMarket Chatbot API",
        version="1.0.0",
        description="API for RealMarket Chatbot",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {"password": {"tokenUrl": "/api/v1/auth/login", "scopes": {}}},
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


frontend_path = Path(__file__).parent.parent / "frontend_dist"
app.mount("/static", StaticFiles(directory="frontend/dist", html=True), name="static")


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
