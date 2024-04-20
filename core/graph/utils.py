import networkx as nx

from core.models import Edge, Node


async def nodes_relation_checker(nodes: list[Node], edges: list[Edge]) -> bool:
    G = nx.DiGraph()

    for node in nodes:
        G.add_node(node)

    for edge in edges:
        G.add_edge(
            edge.source_node_id,
            edge.destination_node_id,
            condition=edge.condition_type,
        )
    start_node = next(
        (node for node in nodes if node.type == "Start Node"), None
    )
    end_node = next((node for node in nodes if node.type == "End Node"), None)

    return nx.has_path(G, start_node, end_node)
