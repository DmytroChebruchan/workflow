from sqlalchemy.ext.asyncio import AsyncSession

from api.edges.scripts import delete_edges_of_node_script, edge_creator_script
from api.general.utils_ElementRepo import ElementRepo
from api.nodes.schemas.schemas_by_nodes_creating_stage import NodeUpdate
from api.nodes.validation.script import nodes_val_with_pydentic_script
from core.models.node import Node


class NodeManagement(ElementRepo):
    """Managing node based on ElementRepo."""

    model = Node

    def __init__(self, session: AsyncSession, node_id: int | None = None):
        super().__init__(session=session, model=self.model)
        if node_id is not None:
            self.node_id = node_id

    async def get_node_by_id(self, node_id: int | None = None) -> Node:
        if node_id is not None:
            self.node_id = node_id
        self.object_of_class = await self.get_element_by_id(
            element_id=self.node_id,
        )
        return self.object_of_class

    async def update_node(self, node_update: NodeUpdate) -> Node:
        # Validate the updated node fields
        await nodes_val_with_pydentic_script(
            data=node_update.model_dump(), session=self.session
        )

        # get node
        self.object_of_class = await self.get_node_by_id()

        # Update the node fields
        for field, value in node_update.model_dump(exclude_unset=True).items():
            setattr(self.object_of_class, field, value)

        await self.commit_and_refresh_element()

        # update edges related
        await self.update_edges_of_node(node_update=node_update)

        return self.object_of_class

    async def delete_node(self, node_id: int = None) -> None:
        if node_id is not None:
            await self.get_node_by_id(node_id)
        await self.object_of_class.delete_element_from_db()

    async def update_edges_of_node(self, node_update: NodeUpdate) -> None:
        # delete edges of the node
        await delete_edges_of_node_script(
            session=self.session, node=self.object_of_class
        )
        # create new edges
        await edge_creator_script(
            node_id=node_update.id,
            node_in=node_update,
            session=self.session,
        )
