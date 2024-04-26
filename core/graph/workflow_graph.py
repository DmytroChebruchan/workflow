from typing import List

import networkx as nx
from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import get_element_by_id
from api.nodes.node_attr_values import NodeType
from core.models import Edge, Node


class WorkflowGraph:
    """
    Class to represent a workflow graph.
    """

    def __init__(
        self, nodes: List[Node], edges: List[Edge], session: AsyncSession
    ):
        self.nodes = nodes
        self.edges = edges
        self.session = session
        self.graph: nx.DiGraph = nx.DiGraph()
        self.start_node = None
        self.end_node = None

    async def async_update_graph(self):
        """
        Asynchronously update the graph by adding edges, nodes,
         and calculating the path.
        """
        await self._add_edges()
        await self._add_nodes()
        await self._update_important_nodes_by_type()

    async def _add_nodes(self):
        """
        Asynchronously add nodes to the graph.
        """
        self.graph.add_nodes_from(self.nodes)

    async def _add_edges(self):
        """
        Asynchronously add edges to the graph.
        """
        for edge in self.edges:
            node_from = await self._get_node_by_id(edge.source_node_id)
            node_to = await self._get_node_by_id(edge.destination_node_id)
            self.graph.add_edge(
                node_from, node_to, condition=edge.condition_type
            )

    async def _update_important_nodes_by_type(self):
        """
        Asynchronously update start and end nodes by their types.
        """
        self.start_node = await self._get_node_by_type(
            node_type=NodeType.START
        )
        self.end_node = await self._get_node_by_type(node_type=NodeType.END)

    async def has_path(self):
        """
        Asynchronously check if there is a path between start and end nodes.
        """
        return nx.has_path(self.graph, self.start_node, self.end_node)

    async def path_steps_generator(self):
        """
        Asynchronously generate the steps of the path.
        """
        path = nx.shortest_path(self.graph, self.start_node, self.end_node)
        steps = [{"type": "node", "value": path[0]}]
        for i in range(1, len(path)):
            edge = self.graph.get_edge_data(path[i - 1], path[i])
            if edge:
                steps.append(
                    {
                        "type": "edge",
                        "value": {"condition_of_edge": edge["condition"]},
                    }
                )
            steps.append({"type": "node", "value": path[i]})
        return steps

    async def find_path(self) -> dict:
        """
        Asynchronously get the path details.
        """
        # Check if there is a path between the start and end nodes
        if await self.has_path():
            # Find the shortest path
            return {
                "has_path": True,
                "path": await self.path_steps_generator(),
            }
        else:
            return {
                "has_path": False,
                "comments": "No path exists between the Start and End nodes.",
            }

    async def _get_node_by_id(self, node_id: int) -> Node:
        return await get_element_by_id(
            element_id=node_id, element=Node, session=self.session
        )

    async def _get_node_by_type(self, node_type: NodeType) -> Node | None:
        return next(
            (node for node in self.nodes if node.type == node_type), None
        )
