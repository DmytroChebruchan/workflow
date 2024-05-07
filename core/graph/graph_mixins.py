import networkx as nx

from core.graph.schemas.workflow_graph_base import WorkflowGraphBase
from core.graph.utils import (
    edge_step_generator,
    node_step_generator,
    node_dict_generator,
)


class WorkFindMixinGraph(WorkflowGraphBase):
    """
    Mixin for finding path a workflow graph.
    """

    async def has_path(self):
        """
        Asynchronously check if there is a path between start and end nodes.
        """
        return nx.has_path(self.graph, self.start_node, self.end_node)

    async def path_steps_generator(self):
        """
        Asynchronously generate the steps of the path.
        """
        path = await self.shortest_path_finder()

        first_node = await node_dict_generator(path[0])
        steps = [{"type": "node", "value": first_node}]
        for i in range(1, len(path)):
            edge = self.graph.get_edge_data(path[i - 1], path[i])
            if edge:
                await edge_step_generator(edge, steps)
            await node_step_generator(node=path[i], steps=steps)
        return steps

    async def shortest_path_finder(self):
        return nx.shortest_path(
            G=self.graph, source=self.start_node, target=self.end_node
        )

    async def find_path(self) -> dict:
        """
        Asynchronously get the path details.
        """
        has_path = await self.has_path()
        # Check if there is a path between the start and end nodes
        if has_path:
            # Find the shortest path
            return {
                "has_path": has_path,
                "path": await self.path_steps_generator(),
            }
        return {
            "has_path": has_path,
            "comments": "No path exists between the Start and End nodes.",
        }
