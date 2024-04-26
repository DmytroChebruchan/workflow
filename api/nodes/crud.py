from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.edges.crud import creating_required_edges
from api.general.utils import (
    commit_and_refresh_element,
    delete_element_from_db,
    get_element_by_id,
)
from api.nodes.node_handling import delete_edges_of_node
from api.nodes.schemas.schemas import NodeCreate, NodeUpdate
from api.nodes.utils import node_model_dict_generator, node_saver
from api.nodes.validation_with_pydentic import nodes_validation_with_pydentic
from core.models.node import Node


async def create_node(session: AsyncSession, node_in: NodeCreate) -> Node:
    # validation
    await nodes_validation_with_pydentic(node_in.model_dump())

    # node saver
    node_model_dict = await node_model_dict_generator(node_in)
    node = await node_saver(node_model_dict, session)

    # create edges
    await creating_required_edges(node=node, node_in=node_in, session=session)
    return node


async def get_node_by_id(session: AsyncSession, node_id: int) -> Node:
    return await get_element_by_id(
        element=Node,
        session=session,
        element_id=node_id,
    )


async def delete_node_by_id(session: AsyncSession, node_id: int) -> None:
    node = await get_element_by_id(
        session=session, element_id=node_id, element=Node
    )
    if node is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Node with ID {node_id} not found",
        )
    await delete_edges_of_node(session=session, node=node)
    await delete_element_from_db(session=session, element=node)


async def update_node(
    session: AsyncSession, node_id: int, node_update: NodeUpdate
) -> Node:

    # Validate the updated node fields
    await nodes_validation_with_pydentic(node_update.model_dump())

    # Validate existence of node
    node = await get_element_by_id(
        session=session,
        element_id=node_id,
        element=Node,
    )

    # Update the node fields
    for field, value in node_update.model_dump(exclude_unset=True).items():
        setattr(node, field, value)

    await commit_and_refresh_element(session=session, element=node)
    return node
