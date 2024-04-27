from typing import Optional

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from api.edges.schemas import EdgeBase
from api.general.utils import (
    commit_and_refresh_element,
    delete_element_from_db,
    get_element_by_id,
    save_element_into_db,
)
from core.models import Node
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


async def read_edge(edge_id: int, session: AsyncSession) -> Optional[Edge]:
    """Read an edge from the database by its ID."""
    # Retrieve the edge from the database
    edge = await get_element_by_id(
        element_id=edge_id,
        session=session,
        element=Edge,
    )
    return edge


async def creating_required_edges(
    node_id: int,
    node_from_id: int | None,
    nodes_to_list: list,
    session: AsyncSession,
) -> None:
    if node_from_id:
        await create_edge(
            from_node_id=node_from_id,
            to_node_id=node_id,
            session=session,
        )

    if nodes_to_list:
        for node_to in nodes_to_list:
            await create_edge(
                from_node_id=node_id,
                to_node_id=node_to["id"],
                session=session,
                condition=node_to["condition"],
            )


async def delete_edge_by_id(edge_id: int, session: AsyncSession) -> None:
    edge = await get_element_by_id(
        session=session, element_id=edge_id, element=Edge
    )
    await delete_element_from_db(session=session, element=edge)


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
    node_from_id: int | None, nodes_to_list: list, session: AsyncSession
) -> None:
    edges_to_check = [
        (node_from_id, node_to["id"]) for node_to in nodes_to_list
    ]

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
