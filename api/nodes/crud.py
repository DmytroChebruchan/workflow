from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import (
    commit_and_refresh_element,
    get_element_by_id,
)
from api.nodes.schemas.schemas import NodeUpdate
from api.nodes.validation.script import nodes_val_with_pydentic_script
from core.models.node import Node


async def get_node_by_id(session: AsyncSession, node_id: int) -> Node:
    return await get_element_by_id(
        element=Node,
        session=session,
        element_id=node_id,
    )


async def update_node(
    session: AsyncSession, node_id: int, node_update: NodeUpdate
) -> Node:

    # Validate the updated node fields
    await nodes_val_with_pydentic_script(
        data=node_update.model_dump(), session=session
    )

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
