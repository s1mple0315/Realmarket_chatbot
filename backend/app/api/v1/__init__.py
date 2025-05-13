from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .assistant import router as assistant_router
from .files import router as files_router
from .widget import router as widget_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(assistant_router, tags=["assistant"])
router.include_router(files_router, prefix="/files", tags=["files"])
router.include_router(widget_router, prefix="/widget", tags=["widget"])
