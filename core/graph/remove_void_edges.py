import networkx as nx

from api.nodes.schemas.schemas_node_by_type import ConditionNode


async def clean_graph_from_void_edges(graph: nx.DiGraph) -> nx.DiGraph:
    edges_to_remove = await void_edges_finder(graph)
    graph.remove_edges_from(edges_to_remove)
    return graph


async def void_edges_finder(graph: nx.DiGraph) -> list:
    condition_nodes = [
        node for node in graph.nodes if node.type == "Condition Node"
    ]

    if len(graph.nodes) < 4 or not condition_nodes:
        return []

    edges_to_remove = []
    for node in condition_nodes:
        edge = await void_edge_finder(graph, node)
        if edge is not None:
            edges_to_remove.append(edge)
    return edges_to_remove


async def void_edge_finder(
    graph: nx.DiGraph, node: ConditionNode
) -> list[tuple]:
    condition_of_void_edge = await condition_of_edge_to_be_removed(graph, node)
    return [
        (u, v, c)
        for u, v, c in graph.edges(data="condition")
        if (u == node or v == node) and (c == condition_of_void_edge)
    ]


async def condition_of_edge_to_be_removed(graph: nx.DiGraph, node) -> bool:
    condition_of_msg_node = await predecessor_msg_status_finder(graph, node)
    return not node.condition == condition_of_msg_node


async def predecessor_msg_status_finder(graph: nx.DiGraph, node) -> str:
    msg_node_predecessor = list(graph.predecessors(node))[0]
    return (
        msg_node_predecessor.status
        if msg_node_predecessor.type == "Message Node"
        else await predecessor_msg_status_finder(graph, msg_node_predecessor)
    )
