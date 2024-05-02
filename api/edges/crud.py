from sqlalchemy.ext.asyncio import AsyncSession

from api.edges.schemas import EdgeBase
from api.general.utils_element_class import ElementManagement
from core.models.edge import Edge


class EdgeManagement:
    def __init__(
        self, session: AsyncSession, condition: bool, direction: dict
    ):
        self.session = session
        self.condition = condition
        self.direction = direction

    async def create_edge(self) -> Edge:
        validated_edge = EdgeBase(
            source_node_id=self.direction["from"],
            destination_node_id=self.direction["to"],
            condition_type=self.condition,
        )
        return await self.save_edge_into_db(validated_edge)

    async def save_edge_into_db(self, validated_edge):
        edge = Edge(**validated_edge.model_dump())
        element = ElementManagement(
            session=self.session, model=Edge, class_object=edge
        )
        return await element.save_element_into_db()
