import networkx as nx
import rule_engine
from api.nodes.schemas.schemas_node_by_type import ConditionNode


def clean_graph_from_void_edges(graph: nx.DiGraph) -> nx.DiGraph:
    edges_to_remove = void_edges_finder(graph)
    if not edges_to_remove:
        return graph
    graph.remove_edges_from(edges_to_remove)
    return graph


def void_edges_finder(graph: nx.DiGraph) -> list[tuple]:
    condition_nodes = [
        node for node in graph.nodes if node.type == "Condition Node"
    ]

    if len(graph.nodes) < 4 or not condition_nodes:
        return []

    edges_to_remove = []
    for node in condition_nodes:
        edge = void_edge_finder(graph, node)
        if edge is not None:
            edges_to_remove.append(edge)
    return edges_to_remove


def void_edge_finder(graph: nx.DiGraph, node: ConditionNode) -> tuple:
    condition_of_void_edge = condition_of_edge_to_be_removed(graph, node)
    rule = rule_engine.Rule(f"condition == {condition_of_void_edge}")
    edges = [
        {"from": u, "to": v, "condition": bool(c)}
        for u, v, c in graph.edges(data="condition")
    ]
    void_edge = rule.filter(edges)[0]
    return void_edge["from"], void_edge["to"], void_edge["condition"]


def condition_of_edge_to_be_removed(graph: nx.DiGraph, node) -> bool:
    condition_of_msg_node = predecessor_msg_status_finder(graph, node)
    return not node.condition == condition_of_msg_node


def predecessor_msg_status_finder(graph: nx.DiGraph, node) -> str:
    msg_node_predecessor = list(graph.predecessors(node))[0]
    return (
        msg_node_predecessor.status
        if msg_node_predecessor.type == "Message Node"
        else predecessor_msg_status_finder(graph, msg_node_predecessor)
    )
