from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import get_element_by_id, get_elements
from api.nodes import crud
from api.nodes.schemas.schemas import NodeCreate, NodeFromDB, NodeUpdate
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
) -> NodeFromDB | None:
    return await crud.create_node(session=session, node_in=node_in)


@router.get("/details/{node_id}/", response_model=NodeFromDB)
async def get_node_view(
    node_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> NodeFromDB:
    node = await get_element_by_id(
        session=session,
        element_id=node_id,
        element=NodeFromDB,
    )
    if node:
        return node
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Node {node_id} not found!",
    )


@router.delete("/{node_id}/")
async def delete_node_view(
    node_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    await crud.delete_node_by_id(session=session, node_id=node_id)
    return Response(content={"status": "ok"}, status_code=200)


@router.put("/{node_id}/")
async def update_node_view(
    node_id: int,
    node_update: NodeUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    await crud.update_node(
        session=session,
        node_id=node_id,
        node_update=node_update,
    )
    return Response(
        content={"status": "ok"},
        status_code=200,
    )
