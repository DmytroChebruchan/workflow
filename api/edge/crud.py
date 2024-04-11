from sqlalchemy.ext.asyncio import AsyncSession

from api.edge.schemas import EdgeBase


async def create_edge(
    from_node_id: int, to_node_id: int, session: AsyncSession
):
    edge = EdgeBase(
        source_node_id=from_node_id,
        destination_node_id=to_node_id,
    )
    session.add(edge)
    await session.commit()
    return edge
