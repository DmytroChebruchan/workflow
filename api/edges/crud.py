from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from api.edges.schemas import EdgeBase
from api.general.utils import (
    commit_and_refresh_element,
    delete_element_from_db,
    get_element_by_id,
    save_element_into_db,
)
from api.nodes.schemas.schemas import NodeCreate
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
    node: Node,
    node_in: NodeCreate,
    session: AsyncSession,
) -> None:
    if node_in.from_node_id:
        await create_edge(
            from_node_id=node_in.from_node_id,
            to_node_id=node.id,
            session=session,
        )

    if node_in.nodes_to_list:
        for node_to in node_in.nodes_to_list:
            await create_edge(
                from_node_id=node.id,
                to_node_id=node_to["id"],
                session=session,
                condition=node_to["condition"],
            )


async def delete_edge(edge_id: int, session: AsyncSession) -> None:
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
