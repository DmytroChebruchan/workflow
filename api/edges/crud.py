from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from api.edges.schemas import EdgeBase
from api.nodes.validators import node_validator
from core.models.edge import Edge


async def create_edge(
    from_node_id: int,
    to_node_id: int,
    session: AsyncSession,
    condition: Optional[bool] = True,
) -> Edge:

    # Retrieve source and destination nodes
    await node_validator(from_node_id, session)
    await node_validator(to_node_id, session)

    # Create and persist the edges
    edge = Edge(
        source_node_id=from_node_id,
        destination_node_id=to_node_id,
        condition_type=condition,
    )
    session.add(edge)
    await session.commit()
    await session.refresh(edge)

    return edge
