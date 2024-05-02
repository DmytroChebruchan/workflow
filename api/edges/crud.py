from sqlalchemy import delete, or_
from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import get_element_by_id, save_element_into_db
from api.workflows.crud import get_workflow_by_id
from core.models import Node, Edge
from core.models.edge import Edge


async def create_edge(
    from_node_id: int,
    to_node_id: int,
    session: AsyncSession,
    condition: bool,
) -> Edge:
    await get_element_by_id(
        session=session,
        element_id=from_node_id,
        element=Node,
    )
    await get_element_by_id(
        session=session,
        element_id=to_node_id,
        element=Node,
    )
    # Create and persist the edges
    edge = Edge(
        source_node_id=from_node_id,
        destination_node_id=to_node_id,
        condition_type=condition,
    )
    return await save_element_into_db(session=session, element=edge)


async def creating_required_edges(
    node_id: int,
    node_from_id: int | None,
    nodes_destination_dict: dict,
    session: AsyncSession,
) -> None:
    if node_from_id:
        await create_edge(
            from_node_id=node_from_id,
            to_node_id=node_id,
            session=session,
            condition=True,
        )

    if nodes_destination_dict:
        for key in nodes_destination_dict:
            await create_edge(
                from_node_id=node_id,
                to_node_id=nodes_destination_dict[key],
                session=session,
                condition=key,
            )


async def delete_old_edges(
    node_from_id: int | None,
    nodes_destination: dict | None,
    session: AsyncSession,
    edge_condition_type: bool,
) -> None:
    if node_from_id:
        await session.execute(
            delete(Edge).where(
                (Edge.source_node_id == node_from_id)
                and (Edge.condition_type == edge_condition_type)
            )
        )

    if nodes_destination:
        destination_node_ids = [
            node_to for node_to in nodes_destination.values()
        ]

        # Delete edges that match the conditions
        await session.execute(
            delete(Edge).where(
                (Edge.source_node_id == node_from_id)
                and (Edge.destination_node_id.in_(destination_node_ids))
            )
        )
    await session.commit()


async def delete_edges_of_workflow(workflow_id: int, session: AsyncSession):
    workflow = await get_workflow_by_id(
        session=session, workflow_id=workflow_id
    )
    nodes_related = workflow.nodes
    nodes_ids = [node.id for node in nodes_related]

    # Construct a list of conditions for source and destination node IDs
    conditions = or_(
        Edge.source_node_id.in_(nodes_ids),
        Edge.destination_node_id.in_(nodes_ids),
    )

    # Construct a delete statement with the combined conditions
    stmt = delete(Edge).where(conditions)

    # Execute the delete statement and commit the changes
    await session.execute(stmt)
    await session.commit()
