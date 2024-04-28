from sqlalchemy.ext.asyncio import AsyncSession

from api.edges.crud import (
    creating_required_edges,
    delete_edges_of_workflow,
    delete_old_edges,
)
from api.nodes.crud import delete_nodes_of_workflow
from api.nodes.schemas.schemas import NodeCreate
from api.nodes.utils import node_saver
from api.nodes.validation_with_pydentic import nodes_validation_with_pydentic
from core.models import Node


async def create_node_script(
    session: AsyncSession, node_in: NodeCreate
) -> Node:
    nodes_dest_json_dict = node_in.nodes_dest_dict
    if nodes_dest_json_dict:
        node_in.nodes_dest_dict = {
            bool(k.capitalize()): v for k, v in nodes_dest_json_dict.items()
        }
    # validation
    await nodes_validation_with_pydentic(node_in.model_dump())

    if node_in.from_node_id or node_in.nodes_dest_dict:
        await delete_old_edges(
            node_from_id=node_in.from_node_id,
            nodes_destination=node_in.nodes_dest_dict,
            session=session,
            edge_condition_type=node_in.edge_condition_type,
        )

    # node saver
    node = await node_saver(node_in, session)

    # create edges
    if node_in.from_node_id or node_in.nodes_dest_dict:
        await creating_required_edges(
            node_id=node.id,
            node_from_id=node_in.from_node_id,
            nodes_destination_dict=node_in.nodes_dest_dict,
            session=session,
        )
    return node


async def delete_nodes_of_workflow_script(
    session: AsyncSession, workflow_id: int
) -> None:
    # Get the list of deleted node IDs
    await delete_edges_of_workflow(session=session, workflow_id=workflow_id)
    # Delete nodes of the specified workflow
    await delete_nodes_of_workflow(session=session, workflow_id=workflow_id)
