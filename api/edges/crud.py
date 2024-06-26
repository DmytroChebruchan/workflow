from sqlalchemy.ext.asyncio import AsyncSession

from api.edges.schemas import EdgeBase
from api.general.utils_ElementRepo import ElementRepo
from core.models.edge import Edge


class EdgeRepo(ElementRepo):
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
        self.object_of_class = Edge(**validated_edge.model_dump())
        return await self.save_element_into_db()
