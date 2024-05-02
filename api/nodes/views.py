from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import get_elements
from api.nodes.crud import (
    get_node_by_id,
    update_node,
)
from api.nodes.schemas.schemas import NodeCreate, NodeFromDB, NodeUpdate
from api.nodes.scripts import create_node_script, delete_node_by_id_script
from core.database.database import get_async_session
from core.models.node import Node as NodeModel

router = APIRouter(tags=["Nodes"])


@router.get("/show_nodes/", response_model=List[NodeFromDB])
async def get_nodes_view(
    session: AsyncSession = Depends(get_async_session),
):
    return await get_elements(session=session, element=NodeModel)


@router.post("/create/", response_model=NodeFromDB)
async def create_node_view(
    node_in: NodeCreate,
    session: AsyncSession = Depends(get_async_session),
) -> NodeModel | None:
    return await create_node_script(session=session, node_in=node_in)


@router.get("/read/{node_id}/", response_model=NodeFromDB)
async def get_node_view(
    node_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> NodeModel:
    return await get_node_by_id(
        session=session,
        node_id=node_id,
    )


@router.delete("/{node_id}/")
async def delete_node_view(
    node_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> dict[str, str]:
    await delete_node_by_id_script(session=session, node_id=node_id)
    return {"message": "Node deleted!"}


@router.put("/{node_id}/")
async def update_node_view(
    node_id: int,
    node_update: NodeUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> dict[str, str]:
    await update_node(
        session=session,
        node_id=node_id,
        node_update=node_update,
    )
    return {"message": "Node updated!"}
