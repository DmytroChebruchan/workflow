from fastapi import APIRouter

from .general.views import router as general_router
from .nodes.views import router as node_router
from .workflows.views import router as workflow_router

router = APIRouter()
router.include_router(router=workflow_router, prefix="/workflows")
router.include_router(router=node_router, prefix="/nodes")
router.include_router(router=general_router, prefix="")
