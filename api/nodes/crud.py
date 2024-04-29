from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import (
    commit_and_refresh_element,
    delete_element_from_db,
    get_element_by_id,
)
from api.nodes.node_handling import delete_edges_of_node
from api.nodes.schemas.schemas import NodeUpdate
from api.nodes.validation_with_pydentic import nodes_validation_with_pydentic
from core.models.node import Node


async def get_node_by_id(session: AsyncSession, node_id: int) -> Node:
    return await get_element_by_id(
        element=Node,
        session=session,
        element_id=node_id,
    )


async def delete_node_by_id_script(
    session: AsyncSession, node_id: int
) -> None:
    node = await get_node_by_id(session=session, node_id=node_id)
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


async def delete_nodes_of_workflow(
    session: AsyncSession, workflow_id: int
) -> None:
    await session.execute(delete(Node).where(Node.workflow_id == workflow_id))
    await session.commit()
