from sqlalchemy.ext.asyncio import AsyncSession

from api.edges.schemas import EdgeBase
from api.general.utils import save_element_into_db
from core.models.edge import Edge


async def create_edge(
    direction: dict,
    session: AsyncSession,
    condition: bool,
) -> Edge:
    validated_edge = EdgeBase(
        source_node_id=direction["from"],
        destination_node_id=direction["to"],
        condition_type=condition,
    )
    edge = Edge(**validated_edge.model_dump())
    return await save_element_into_db(session=session, element=edge)
