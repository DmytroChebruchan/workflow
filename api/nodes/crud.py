from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import (
    commit_and_refresh_element,
)
from api.general.utils_element_class import ElementManagement
from api.nodes.schemas.schemas import NodeUpdate
from api.nodes.validation.script import nodes_val_with_pydentic_script
from core.models.node import Node


async def get_node_by_id(session: AsyncSession, node_id: int) -> Node:
    element = ElementManagement(session=session, model=Node)
    return await element.get_element_by_id(
        element_id=node_id,
    )


async def update_node(
    session: AsyncSession, node_id: int, node_update: NodeUpdate
) -> Node:

    # Validate the updated node fields
    await nodes_val_with_pydentic_script(
        data=node_update.model_dump(), session=session
    )
    element = ElementManagement(session=session, model=Node)
    node = element.get_element_by_id(element_id=node_id)

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
