from sqlalchemy.ext.asyncio import AsyncSession

from api.edges.schemas import EdgeBase
from api.general.utils_element_class import ElementManagement
from core.models.edge import Edge


class EdgeManagement(ElementManagement):
    model = Edge

    def __init__(
        self, session: AsyncSession, condition: bool, direction: dict
    ):
        super().__init__(session=session, model=self.model)
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
        self.object_of_class = Edge(**validated_edge.model_dump())
        return await self.save_element_into_db()
