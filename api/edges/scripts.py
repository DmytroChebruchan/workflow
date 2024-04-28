from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import get_element_by_id, save_element_into_db
from core.models import Node, Edge


async def create_edge_script(
    condition: bool, from_node_id: int, session: AsyncSession, to_node_id: int
):
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
