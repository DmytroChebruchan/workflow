from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from api.nodes.schemas import Node, NodeCreate
from api.nodes import crud
from api.workflows.crud import get_workflow_by_id

router = APIRouter(tags=["Nodes"])


@router.get("/show_nodes/", response_model=list[Node])
async def get_nodes_view(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_nodes(session=session)


@router.post("/create/", response_model=Node)
async def create_node(
    node_in: NodeCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Node | None:
    workflow = await get_workflow_by_id(
        session=session, workflow_id=node_in.workflow_id
    )
    if workflow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow with ID {node_in.workflow_id} not found",
        )
    return await crud.create_node(session=session, node_in=node_in)


@router.get("/{node_id}/", response_model=Node)
async def get_nodes_view(
    node_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    node = await crud.get_node_by_id(
        session=session,
        node_id=node_id,
    )
    if node is not None:
        return node

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Node {node_id} not found!",
    )


@router.delete("/{node_id}/", response_model=None)
async def delete_node(
    node_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_node_by_id(session=session, node_id=node_id)
