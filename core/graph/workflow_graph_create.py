from typing import List

import networkx as nx
from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import get_element_by_id
from api.nodes.node_attr_values import NodeType
from core.graph.remove_void_edges import clean_graph_from_void_edges
from core.graph.schemas.workflow_graph_base import WorkflowGraphBase
from core.models import Edge, Node


class WorkflowGraphCreator(WorkflowGraphBase):
    """
    Class to represent a workflow graph.
    """

    def __init__(
        self, nodes: List[Node], edges: List[Edge], session: AsyncSession
    ):
        self.graph: nx.DiGraph = nx.DiGraph()
        self.nodes = nodes
        self.edges = edges
        self.session = session
        self.graph_generator()

    def graph_generator(self):
        self.graph.add_nodes_from(self.nodes)
        self._add_edges()
        self._update_important_nodes_by_type_sync()
        self._remove_void_edges()

    def _add_edges(self):
        """
        Asynchronously add edges to the graph.
        """
        for edge in self.edges:
            node_from = [
                node for node in self.nodes if node.id == edge.source_node_id
            ][0]
            node_to = [
                node
                for node in self.nodes
                if node.id == edge.destination_node_id
            ][0]
            self.graph.add_edge(
                node_from, node_to, condition=edge.condition_type
            )

    def _update_important_nodes_by_type_sync(self):
        """
        Asynchronously update start and end nodes by their types.
        """
        self.start_node = [
            node for node in self.nodes if node.type == "Start Node"
        ][0]
        self.end_node = [
            node for node in self.nodes if node.type == "End Node"
        ][0]

    async def _get_node_by_id(self, node_id: int) -> Node:
        return await get_element_by_id(
            element_id=node_id, element=Node, session=self.session
        )

    async def _get_node_by_type(self, node_type: NodeType) -> Node | None:
        return next(
            (node for node in self.nodes if node.type == node_type), None
        )

    def _remove_void_edges(self):
        """removes edges of Condition nodes that are void"""
        self.graph = clean_graph_from_void_edges(self.graph)
