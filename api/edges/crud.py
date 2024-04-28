from typing import Optional
from sqlalchemy import or_
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from api.edges.schemas import EdgeBase
from api.general.utils import (
    commit_and_refresh_element,
    delete_element_from_db,
    get_element_by_id,
    save_element_into_db,
)
from api.workflows.crud import get_workflow_by_id
from core.models import Node, Edge
from core.models.edge import Edge


async def create_edge(
    from_node_id: int,
    to_node_id: int,
    session: AsyncSession,
    condition: Optional[bool] = True,
) -> Edge:

    # Check source and destination nodes
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
    nodes_destination_list: list,
    session: AsyncSession,
) -> None:
    if node_from_id:
        await create_edge(
            from_node_id=node_from_id,
            to_node_id=node_id,
            session=session,
        )

    if nodes_destination_list:
        for node_to in nodes_destination_list:
            await create_edge(
                from_node_id=node_id,
                to_node_id=node_to["id"],
                session=session,
                condition=node_to["condition"],
            )


async def update_edge(
    edge_id: int, edge_update: EdgeBase, session: AsyncSession
) -> None:
    edge = await get_element_by_id(
        session=session, element_id=edge_id, element=Edge
    )

    # Update the node fields
    for field, value in edge_update.dict(exclude_unset=True).items():
        setattr(edge, field, value)

    await commit_and_refresh_element(session=session, element=edge)
    return edge


async def delete_old_edges(
    node_from_id: int | None,
    nodes_destination_list: list,
    session: AsyncSession,
) -> None:
    edges_to_check = [
        (node_from_id, node_to["id"]) for node_to in nodes_destination_list
    ]
    if not edges_to_check:
        return

    # Extract destination node IDs from edges_to_check
    destination_node_ids = [node_id for _, node_id in edges_to_check]

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
