from sqlalchemy.ext.asyncio import AsyncSession

from api.edges.schemas import EdgeBase
from api.general.utils_element_class import ElementManagement
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
    element = ElementManagement(session=session, model=Edge, class_object=edge)
    return await element.save_element_into_db()
