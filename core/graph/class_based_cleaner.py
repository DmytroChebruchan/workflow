import networkx as nx

from api.nodes.schemas.schemas_node_by_type import ConditionNode


class GraphCleaner:
    graph: nx.DiGraph

    async def clean_graph_from_void_edges(self):
        edges_to_remove = await self.void_edges_finder()
        self.graph.remove_edges_from(edges_to_remove)

    async def void_edges_finder(self) -> list:
        condition_nodes = [
            node for node in self.graph.nodes if node.type == "Condition Node"
        ]

        if len(self.graph.nodes) < 4 or not condition_nodes:
            return []

        edges_to_remove = []
        for node in condition_nodes:
            edge = await self.void_edge_finder(node)
            if edge is not None:
                edges_to_remove.append(edge)
        return edges_to_remove

    async def void_edge_finder(self, node: ConditionNode) -> list[tuple]:
        condition_of_void_edge = await self.condition_of_edge_to_be_removed(
            node
        )
        return [
            (u, v, c)
            for u, v, c in self.graph.edges(data="condition")
            if (u == node or v == node) and (c == condition_of_void_edge)
        ]

    async def condition_of_edge_to_be_removed(self, node) -> bool:
        condition_of_msg_node = await self.predecessor_msg_status_finder(node)
        return not node.condition == condition_of_msg_node

    async def predecessor_msg_status_finder(self, node) -> str:
        msg_node_predecessor = list(self.graph.predecessors(node))[0]
        return (
            msg_node_predecessor.status
            if msg_node_predecessor.type == "Message Node"
            else await self.predecessor_msg_status_finder(msg_node_predecessor)
        )
