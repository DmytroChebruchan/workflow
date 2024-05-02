from sqlalchemy import delete, or_
from sqlalchemy.ext.asyncio import AsyncSession

from api.edges.crud import EdgeManagement
from api.edges.utils import del_destination_edge, delete_edge_from_source
from api.workflows.crud_WorkflowManagement import WorkflowManagement
from core.models import Edge


async def edge_creator_script(node, node_in, session) -> None:
    from_node_avail = node_in.from_node_id
    dest_node_avail = node_in.nodes_dest_dict

    if from_node_avail or dest_node_avail:
        await creating_required_edges_script(
            node_id=node.id,
            node_from_id=node_in.from_node_id,
            nodes_destination_dict=node_in.nodes_dest_dict,
            session=session,
        )


async def creating_required_edges_script(
    node_id: int,
    node_from_id: int | None,
    nodes_destination_dict: dict,
    session: AsyncSession,
) -> None:
    direction = {"from": node_from_id, "to": node_id}
    if node_from_id:
        edge = EdgeManagement(
            session=session, direction=direction, condition=True
        )
        await edge.create_edge()

    if nodes_destination_dict:
        for key in nodes_destination_dict:
            direction = {"from": node_id, "to": nodes_destination_dict[key]}
            edge = EdgeManagement(
                session=session, direction=direction, condition=key
            )
            await edge.create_edge()


async def delete_edges_of_workflow_script(
    workflow_id: int, session: AsyncSession
):
    workflow_object = WorkflowManagement(
        session=session, workflow_id=workflow_id
    )
    workflow = await workflow_object.get_workflow_by_id()

    nodes_ids = [node.id for node in workflow.nodes]

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
    nodes_destination: dict | None,
    session: AsyncSession,
    edge_condition_type: bool,
) -> None:
    if node_from_id:
        await delete_edge_from_source(
            edge_condition_type, node_from_id, session
        )
    if nodes_destination:
        await del_destination_edge(node_from_id, nodes_destination, session)
    await session.commit()
