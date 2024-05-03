from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils_ElementRepo import ElementRepo
from api.nodes.schemas.schemas_by_nodes_creating_stage import NodeUpdate
from api.nodes.validation.script import nodes_val_with_pydentic_script
from core.models.node import Node


class NodeManagement(ElementRepo):
    model = Node

    def __init__(self, session: AsyncSession, node_id: int | None = None):
        super().__init__(session=session, model=self.model)
        if node_id is not None:
            self.node_id = node_id

    async def get_node_by_id(self) -> Node:
        return await self.get_element_by_id(
            element_id=self.node_id,
        )

    async def update_node(self, node_update: NodeUpdate) -> Node:
        # Validate the updated node fields
        await nodes_val_with_pydentic_script(
            data=node_update.model_dump(), session=self.session
        )

        # get node
        self.object_of_class = await self.get_element_by_id(
            element_id=self.node_id
        )

        # Update the node fields
        for field, value in node_update.model_dump(exclude_unset=True).items():
            setattr(self.object_of_class, field, value)

        await self.commit_and_refresh_element()
        return self.object_of_class
