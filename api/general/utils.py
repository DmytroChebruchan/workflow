from core.models import Edge


async def get_edges_of_nodes(nodes: list) -> list[Edge]:
    edges = []
    for node in nodes:
        edges_found = await edges_collector(node)
        edges.extend(edges_found)
    unique_edges_list = list(set(edges))
    return unique_edges_list


async def edges_collector(node):
    edges_found = list(node.outgoing_edges) + list(node.incoming_edges)
    return edges_found
