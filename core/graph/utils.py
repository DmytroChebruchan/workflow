from typing import Dict, List, Union

import networkx as nx

from api.nodes.node_attr_values import NodeType
from core.models import Edge, Node


async def get_path(
    nodes: List[Node],
    edges: List[Edge],
) -> Dict[str, Union[bool, List[str], str]]:
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
        (node for node in nodes if node.type == NodeType.START), None
    )
    end_node = next((node for node in nodes if node.type == NodeType.END), None)

    # Check if there is a path between the start and end nodes
    if nx.has_path(G, start_node, end_node):
        # Find the shortest path
        path = nx.shortest_path(G, start_node, end_node)
        # Construct the list of steps (nodes and edges)
        steps = [path[0]]
        for i in range(1, len(path)):
            edge = G.get_edge_data(path[i - 1], path[i])
            if edge:
                steps.append(edge["condition"])
            steps.append(path[i])
        return {"has_path": True, "path": steps, "comments": "Path found"}
    else:
        return {
            "has_path": False,
            "path": [],
            "comments": "No path exists between the specified nodes",
        }


async def nodes_relation_checker(nodes: list[Node], edges: list[Edge]) -> dict:

    if not nodes or not edges:
        return False

    G = nx.DiGraph()

    await adding_nodes(G, nodes)
    await generate_graph_edges(G, edges, nodes)

    start_node = await node_collector(nodes=nodes, node_type=NodeType.START)
    end_node = await node_collector(nodes=nodes, node_type=NodeType.END)

    has_path = nx.has_path(G, start_node, end_node)

    if has_path:
        result = {"has_path": has_path, "comments": "Path not found"}
    else:
        result = {"has_path": has_path, "comments": "Path found"}
    return result


async def adding_nodes(G: nx.DiGraph, nodes: list[Node]) -> None:
    for node in nodes:
        G.add_node(node)


async def node_collector(nodes: list, node_type: NodeType) -> Node | None:
    start_node = next((node for node in nodes if node.type == node_type), None)
    return start_node


async def generate_graph_edges(G, edges, nodes):
    for edge in edges:
        node_from = next(
            (node for node in nodes if node.id == edge.source_node_id), None
        )
        node_to = next(
            (node for node in nodes if node.id == edge.destination_node_id),
            None,
        )
        G.add_edge(node_from, node_to, condition=edge.condition_type)

    return G
