from sqlalchemy.ext.asyncio import AsyncSession

from api.edges.scripts import (
    delete_edges_of_workflow_script,
    delete_old_edges_script,
    edge_creator_script,
    delete_edges_of_node_script,
)
from api.nodes.crud_NodeManagement import NodeManagement
from api.nodes.node_handling import delete_nodes_of_workflow
from api.nodes.schemas.schemas_by_nodes_creating_stage import NodeCreate
from api.nodes.utils import node_saver
from api.nodes.validation.script import nodes_val_with_pydentic_script
from core.models import Node


async def create_node_script(
    session: AsyncSession, node_in: NodeCreate
) -> Node:
    """Creates new node, edges in workflow and deletes not used edges."""
    # collecting incoming edge type
    nodes_dest_json_dict = node_in.nodes_dest_dict
    await nodes_dest_update(node_in, nodes_dest_json_dict)

    # validation
    await nodes_val_with_pydentic_script(
        data=node_in.model_dump(), session=session
    )

    # deleting old edges if any
    await trim_inactive_edges_script(node_in, session)

    # node saver
    node = await node_saver(node_in, session)

    # create edges
    await edge_creator_script(node.id, node_in, session)
    return node


async def nodes_dest_update(node_in, nodes_dest_json_dict):
    if nodes_dest_json_dict:
        if (
            "true" not in nodes_dest_json_dict
            and "false" not in nodes_dest_json_dict
        ):
            raise ValueError("Keys of dest_nodes must be only true or false")
        updated_dict = {}
        if "true" in nodes_dest_json_dict:
            updated_dict[True] = nodes_dest_json_dict["true"]
        if "false" in nodes_dest_json_dict:
            updated_dict[False] = nodes_dest_json_dict["false"]
        node_in.nodes_dest_dict = updated_dict


async def trim_inactive_edges_script(node_in, session) -> None:
    """Deletes inactive edges if needed."""
    if (node_in.from_node_id or node_in.nodes_dest_dict) and (
        node_in.edge_condition_type is not None
    ):
        await delete_old_edges_script(
            node_from_id=node_in.from_node_id,
            successors_nodes=node_in.nodes_dest_dict,
            session=session,
            edge_condition_type=node_in.edge_condition_type,
        )


async def delete_nodes_of_workflow_script(
    session: AsyncSession, workflow_id: int
) -> None:
    """Deletes all nodes of workflow."""
    # Get the list of deleted node IDs
    await delete_edges_of_workflow_script(
        session=session, workflow_id=workflow_id
    )
    # Delete nodes of the specified workflow
    await delete_nodes_of_workflow(session=session, workflow_id=workflow_id)


async def delete_node_by_id_script(
    session: AsyncSession, node_id: int
) -> None:
    node_object = NodeManagement(session=session, node_id=node_id)

    # del edges related
    await delete_edges_of_node_script(node_object.object_of_class, session)

    # del element
    await node_object.delete_node()
