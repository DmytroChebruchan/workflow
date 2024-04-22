from typing import Dict, List, Union

import networkx as nx
from matplotlib import pyplot as plt
from networkx import DiGraph
from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import get_element_by_id
from api.nodes.node_attr_values import NodeType
from core.models import Edge, Node


async def get_path(
    nodes: List[Node],
    edges: List[Edge],
    session: AsyncSession,
) -> Dict[str, Union[bool, List[str], str]]:
    G = nx.DiGraph()

    G.add_nodes_from(nodes)
    G = nx.DiGraph()
    await adding_nodes(G, nodes)
    await generate_graph_edges(G, edges, session)

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


async def workflow_graph_checker(
    nodes: list[Node], edges: list[Edge], session
) -> bool:

    if not nodes or not edges:
        return False

    G = await graph_builder(edges, nodes, session)

    start_node = await node_collector(nodes=nodes, node_type=NodeType.START)
    end_node = await node_collector(nodes=nodes, node_type=NodeType.END)

    has_path = nx.has_path(G, start_node, end_node)

    return has_path


async def graph_builder(edges, nodes, session) -> DiGraph:
    G = nx.DiGraph()
    await adding_nodes(G, nodes)
    await generate_graph_edges(G, edges, session)
    nx.draw(G, with_labels=True)
    plt.show()
    return G


async def adding_nodes(G: nx.DiGraph, nodes: list[Node]) -> None:
    for node in nodes:
        G.add_node(node)


async def node_collector(nodes: list, node_type: NodeType) -> Node | None:
    node = next((node for node in nodes if node.type == node_type), None)
    return node


async def generate_graph_edges(G: DiGraph, edges: list, session) -> DiGraph:

    for edge in edges:
        node_from = await get_element_by_id(
            element_id=edge.source_node_id, element=Node, session=session
        )
        node_to = await get_element_by_id(
            element_id=edge.destination_node_id, element=Node, session=session
        )
        G.add_edge(node_from, node_to, condition=edge.condition_type)
    return G
