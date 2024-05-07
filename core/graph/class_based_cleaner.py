import networkx as nx

from api.nodes.schemas.schemas_node_by_type import ConditionNode


class GraphVoidEdgesCleaner:
    """This class provides methods to clean the graph from void edges."""

    graph: nx.DiGraph

    def clean_graph_from_void_edges(self):
        """Edges are considered as void edges if
        edges are linking condition node with successor that has
        void condition of Edge."""
        edges_to_remove = self.void_edges_finder()
        self.graph.remove_edges_from(edges_to_remove)

    def void_edges_finder(self) -> list[tuple]:
        condition_nodes = [
            node for node in self.graph.nodes if node.type == "Condition Node"
        ]

        if len(self.graph.nodes) < 4 or not condition_nodes:
            return []

        edges_to_remove = []
        for node in condition_nodes:
            edge = self.void_edge_finder(node)
            if edge is not None:
                edges_to_remove.append(edge)
        return edges_to_remove

    def void_edge_finder(self, node: ConditionNode) -> tuple[int, int] | None:
        condition_of_void_edge = str(
            self.condition_of_edge_to_be_removed(node)
        )
        void_edge = [
            {"from": u, "to": v, "condition": str(c)}
            for u, v, c in self.graph.edges(data="condition")
            if u.id == node.id and str(c) == condition_of_void_edge
        ][0]
        if not void_edge:
            return None
        return void_edge["from"], void_edge["to"]

    def condition_of_edge_to_be_removed(self, node) -> bool:
        condition_of_msg_node = self.predecessor_msg_status_finder(node)
        return not node.condition == condition_of_msg_node

    def predecessor_msg_status_finder(self, node) -> str:
        msg_node_predecessor = list(self.graph.predecessors(node))[0]
        return (
            msg_node_predecessor.status
            if msg_node_predecessor.type == "Message Node"
            else self.predecessor_msg_status_finder(msg_node_predecessor)
        )
