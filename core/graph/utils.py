from typing import Dict, List, Union

import networkx as nx
from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import get_element_by_id
from api.nodes.node_attr_values import NodeType
from api.nodes.utils import find_node_by_type
from core.models import Node


class WorkflowGraph:
    """
    Class to represent a workflow graph.
    """

    nodes: List
    start_node: Union[None, NodeType]
    end_node: Union[None, NodeType]
    edges: List
    session: AsyncSession
    graph: nx.DiGraph
    has_path: bool
    path_steps: List
    path_details: Dict

    def __init__(self, nodes, edges, session: AsyncSession):
        """
        Initialize the WorkflowGraph.

        Args:
            nodes (list): List of nodes in the graph.
            edges (list): List of edges in the graph.
            session (AsyncSession): Async session for database operations.
        """
        self.nodes = nodes
        self.start_node = None
        self.end_node = None
        self.edges = edges
        self.session = session
        self.graph = nx.DiGraph()
        self.has_path = False
        self.path_steps = []
        self.path_details = {}

    async def async_update_graph(self):
        """
        Asynchronously update the graph by adding edges, nodes,
         and calculating the path.
        """
        await self.add_edges()
        await self.add_nodes()
        await self.update_important_nodes_by_type()
        await self.get_path()

    async def add_nodes(self):
        """
        Asynchronously add nodes to the graph.
        """
        self.graph.add_nodes_from(self.nodes)

    async def add_edges(self):
        """
        Asynchronously add edges to the graph.
        """
        for edge in self.edges:
            node_from = await get_element_by_id(
                element_id=edge.source_node_id,
                element=Node,
                session=self.session,
            )
            node_to = await get_element_by_id(
                element_id=edge.destination_node_id,
                element=Node,
                session=self.session,
            )
            self.graph.add_edge(
                node_from, node_to, condition=edge.condition_type
            )

    async def update_important_nodes_by_type(self):
        """
        Asynchronously update start and end nodes by their types.
        """
        self.start_node = await find_node_by_type(
            nodes=self.nodes, node_type=NodeType.START
        )
        self.end_node = await find_node_by_type(
            nodes=self.nodes, node_type=NodeType.END
        )

    async def has_path_checker(self):
        """
        Asynchronously check if there is a path between start and end nodes.
        """
        if not self.nodes or not self.edges:
            return False
        self.has_path = nx.has_path(self.graph, self.start_node, self.end_node)

    async def path_steps_generator(self):
        """
        Asynchronously generate the steps of the path.
        """
        path = nx.shortest_path(self.graph, self.start_node, self.end_node)

        # Construct the list of steps (nodes and edges)
        steps = await self.steps_generator(path)
        self.path_steps = steps

    async def steps_generator(self, path):
        """
        Asynchronously generate the steps based on the path.
        """
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
            steps.append(path[i])
        return steps

    async def get_path(self):
        """
        Asynchronously get the path details.
        """
        # Check if there is a path between the start and end nodes
        if self.has_path_checker():
            # Find the shortest path
            await self.path_steps_generator()
            self.path_details = {
                "has_path": True,
                "path": self.path_steps,
            }
        else:
            self.path_details = {
                "has_path": False,
                "comments": "No path exists between the Start and End nodes.",
            }
