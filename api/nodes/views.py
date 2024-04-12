from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.nodes import crud
from api.nodes.schemas.schemas import Node, NodeCreate
from api.workflows.validator import workflow_validator
from core.database.database import get_async_session


router = APIRouter(tags=["Nodes"])


@router.get("/show_nodes/", response_model=list[Node])
async def get_nodes_view(
    session: AsyncSession = Depends(get_async_session),
):
    return await crud.get_nodes(session=session)


@router.post("/create/", response_model=Node)
async def create_node_view(
    node_in: NodeCreate,
    session: AsyncSession = Depends(get_async_session),
) -> Node | None:
    await workflow_validator(
        session=session,
        workflow_id=node_in.workflow_id,
    )
    return await crud.create_node(session=session, node_in=node_in)


@router.get("/details/{node_id}/", response_model=Node)
async def get_node_view(
    node_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Node:
    node = await crud.get_node_by_id(session=session, node_id=node_id)
    if node:
        return node
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Node {node_id} not found!",
    )


@router.delete("/{node_id}/", response_model=None)
async def delete_node_view(
    node_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> None:
    await crud.delete_node_by_id(session=session, node_id=node_id)
