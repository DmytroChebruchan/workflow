from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils_ElementRepo import ElementRepo
from api.nodes.node_attr_values import NodeType
from api.nodes.validation.utils import nodes_validation_by_id
from api.nodes.validation.validation_with_pydentic import (
    condition_node_validation,
    node_type_validation,
    node_validation_according_to_type,
)
from core.models import Node


async def nodes_val_with_pydentic_script(
    data: dict, session: AsyncSession
) -> None:
    await node_type_validation(data["type"])
    await node_validation_according_to_type(data, data["type"])
    await condition_node_validation(data=data, session=session)
    await nodes_validation_by_id(
        session=session,
        data=data,
        element=Node,
    )
    await check_edge_to_start_node(
        session=session, nodes_dest_dict=data["nodes_dest_dict"]
    )


async def check_edge_to_start_node(
    session: AsyncSession, nodes_dest_dict: dict
):
    if nodes_dest_dict is None:
        return
    nodes_ids = [nodes_dest_dict[key] for key in nodes_dest_dict]
    for node_id in nodes_ids:
        node_object = ElementRepo(session=session, model=Node)
        node = await node_object.get_element_by_id(element_id=node_id)
        if node.type == NodeType.START:
            raise Exception(
                f"Node {node_id} is Start Node and no edge can point to Start"
                f"Node."
            )
