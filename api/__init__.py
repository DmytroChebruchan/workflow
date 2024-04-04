from fastapi import APIRouter

from .workflows.views import router as workflow_router
from .nodes.views import router as node_router

router = APIRouter()
router.include_router(router=workflow_router, prefix="/workflows")
router.include_router(router=node_router, prefix="/nodes")
