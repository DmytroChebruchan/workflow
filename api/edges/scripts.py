from sqlalchemy import delete, or_
from sqlalchemy.ext.asyncio import AsyncSession

from api.edges.crud import EdgeRepo
from api.edges.utils import (
    delete_destination_edge,
    delete_edge_from_source,
    delete_successors_connecting_edge,
)
from api.general.utils_NodeEdgeManager import EdgeDelManager
from api.nodes.schemas.schemas_by_nodes_creating_stage import (
    NodeCreate,
    NodeUpdate,
)
from api.workflows.crud_WorkflowRepo import WorkflowRepo
from core.models import Edge, Node


async def edge_creator_script(
    node_id: int, node_in: NodeCreate | NodeUpdate, session: AsyncSession
) -> None:
    from_node_avail = node_in.from_node_id
    dest_node_avail = node_in.nodes_dest_dict

    if from_node_avail or dest_node_avail:
        await creating_required_edges_script(
            node_id=node_id,
            node_from_id=node_in.from_node_id,
            nodes_destination_dict=node_in.nodes_dest_dict,
            session=session,
            edge_condition=node_in.edge_condition_type,
        )


async def creating_required_edges_script(
    node_id: int,
    node_from_id: int | None,
    nodes_destination_dict: dict,
    session: AsyncSession,
    edge_condition: bool,
) -> None:
    direction = {"from": node_from_id, "to": node_id}
    if node_from_id:
        edge = EdgeRepo(
            session=session, direction=direction, condition=edge_condition
        )
        await edge.create_edge()

    if nodes_destination_dict:
        for key in nodes_destination_dict:
            direction = {"from": node_id, "to": nodes_destination_dict[key]}
            edge = EdgeRepo(
                session=session, direction=direction, condition=key
            )
            await edge.create_edge()


async def delete_edges_of_workflow_script(
    workflow_id: int, session: AsyncSession
):
    workflow_object = WorkflowRepo(session=session, workflow_id=workflow_id)
    workflow = await workflow_object.get_workflow_by_id()

    nodes_ids = [node.id for node in workflow.nodes]
    if not nodes_ids:
        return
    # Construct a delete statement with the combined conditions
    stmt = delete(Edge).where(
        or_(
            Edge.source_node_id.in_(nodes_ids),
            Edge.destination_node_id.in_(nodes_ids),
        )
    )

    # Execute the delete statement and commit the changes
    await session.execute(stmt)
    await session.commit()


async def delete_old_edges_script(
    node_from_id: int | None,
    successors_nodes: dict | None,
    session: AsyncSession,
    edge_condition_type: bool,
) -> None:
    """This function adds edges to session for delete and then
    deletes them."""
    # deleting edge from predispose
    if node_from_id:
        await delete_edge_from_source(
            edge_condition_type, node_from_id, session
        )
    # deleting edges from source to successor
    if successors_nodes:
        await delete_destination_edge(
            node_from_id=node_from_id,
            successors_nodes=successors_nodes,
            session=session,
        )

        # delete edges between successors
        if len(successors_nodes) == 2:
            await delete_successors_connecting_edge(
                session=session, nodes=successors_nodes
            )
    await session.commit()


async def delete_edges_of_node_script(
    node: Node, session: AsyncSession
) -> None:
    edges_del_object = EdgeDelManager(session=session, node=node)
    await edges_del_object.delete_edges_of_node()
