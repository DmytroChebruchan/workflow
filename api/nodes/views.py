from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils_ElementRepo import ElementRepo
from api.nodes.crud_NodeManagement import NodeManagement
from api.nodes.schemas.schemas import NodeCreate, NodeFromDB, NodeUpdate
from api.nodes.scripts import create_node_script, delete_node_by_id_script
from core.database.database import get_async_session
from core.models.node import Node as NodeModel

router = APIRouter(tags=["Nodes"])


@router.get("/show_nodes/", response_model=List[NodeFromDB])
async def get_nodes_view(
    session: AsyncSession = Depends(get_async_session),
):
    element = ElementRepo(session=session, model=NodeModel)
    return await element.get_elements()


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
    node = NodeManagement(session=session, node_id=node_id)
    return await node.get_node_by_id()


@router.delete("/{node_id}/")
async def delete_node_view(
    node_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> dict[str, str]:
    await delete_node_by_id_script(session=session, node_id=node_id)
    return {"message": "Node was deleted!"}


@router.put("/{node_id}/")
async def update_node_view(
    node_id: int,
    node_update: NodeUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> dict[str, str]:
    node_obj = NodeManagement(session=session, node_id=node_id)
    await node_obj.update_node(
        node_update=node_update,
    )
    return {"message": "Node updated!"}
