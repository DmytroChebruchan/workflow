from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils_ElementRepo import ElementRepo
from api.nodes.schemas.schemas import NodeCreate
from api.nodes.validation.validator import (
    check_node_type_existence_in_workflow,
)
from core.models import Node


async def node_saver(node_in: NodeCreate, session: AsyncSession) -> Node:
    await check_node_type_existence_in_workflow(
        node_in=node_in, session=session
    )
    node = await create_node_from_node_create_dict(node_in)
    element = ElementRepo(session=session, model=Node, object_of_class=node)
    return await element.save_element_into_db()


async def create_node_from_node_create_dict(node_in) -> Node:
    # Extract necessary attributes from the node dictionary
    node_dict = {
        k: v
        for k, v in node_in.model_dump().items()
        if k not in ["nodes_dest_dict", "from_node_id", "edge_condition_type"]
    }

    # Create a new Node object using the extracted attributes
    return Node(**node_dict)
