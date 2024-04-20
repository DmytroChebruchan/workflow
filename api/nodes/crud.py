from select import select
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.edges.crud import creating_required_edges
from api.general.utils import delete_element_from_db, get_element_by_id
from api.nodes.schemas.schemas import NodeCreate, NodeUpdate
from api.nodes.utils import (
    delete_edges_related,
    node_model_dict_generator,
    node_saver,
)
from api.nodes.validation_with_pydentic import nodes_validation_with_pydentic
from api.nodes.validators import validate_existence_of_node
from api.workflows.validator import workflow_validator
from core.models.node import Node


async def create_node(session: AsyncSession, node_in: NodeCreate) -> Node:
    # workflow validation
    await workflow_validator(
        session=session,
        workflow_id=node_in.workflow_id,
    )
    # validation
    await nodes_validation_with_pydentic(node_in.model_dump())

    # node saver
    node_model_dict = await node_model_dict_generator(node_in)
    node = await node_saver(node_model_dict, session)

    # create edges
    await creating_required_edges(node=node, node_in=node_in, session=session)
    return node


async def delete_node_by_id(session: AsyncSession, node_id: int) -> None:
    node = await get_element_by_id(
        session=session, element_id=node_id, element=Node
    )
    if node is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Node with ID {node_id} not found",
        )
    await delete_edges_related(session=session, node=node)
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
    await validate_existence_of_node(node)

    # Update the node fields
    for field, value in node_update.dict(exclude_unset=True).items():
        setattr(node, field, value)

    await session.commit()
    await session.refresh(node)
    return node


async def read_node_by_id(
    session: AsyncSession, node_id: int
) -> Optional[Node]:
    """Read a node from the database by its ID."""
    # Retrieve the node from the database
    query = select(Node).filter(Node.id == node_id)
    result = await session.execute(query)
    node = result.scalar_one_or_none()

    return node
