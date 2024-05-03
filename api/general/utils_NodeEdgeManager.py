from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils_ElementRepo import ElementRepo
from core.models import Node, Edge
from typing import List


class EdgeDelManager:
    def __init__(self, session: AsyncSession, node: Node):
        self.session = session
        self.object_of_class = node

    async def get_edges_of_node(self) -> List[Edge]:
        return list(self.object_of_class.outgoing_edges) + list(
            self.object_of_class.incoming_edges
        )

    async def delete_edges_of_node(self) -> None:
        edges_related = await self.get_edges_of_node()
        for edge in edges_related:
            edge_object = ElementRepo(
                session=self.session, model=Edge, object_of_class=edge
            )
            await edge_object.delete_element_from_db()
