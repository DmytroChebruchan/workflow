from fastapi import APIRouter

from .workflows.views import router as workflow_router

router = APIRouter()
router.include_router(router=workflow_router, prefix="/workflows")
