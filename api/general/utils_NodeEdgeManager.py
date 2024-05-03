from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils_ElementRepo import ElementRepo
from core.models import Node, Edge


class NodeEdgeManager:
    def __init__(self, session: AsyncSession):
        self.session = session


async def get_edges_of_node(node: Node) -> list[Edge]:
    outgoing_edges = list(node.outgoing_edges)
    incoming_edges = list(node.incoming_edges)
    unique_edges = set(outgoing_edges + incoming_edges)
    return list(unique_edges)


async def delete_edges_of_node(node: Node, session: AsyncSession) -> None:
    edges_related = await get_edges_of_node(node=node)
    for edge in edges_related:
        element = ElementRepo(
            session=session, model=Edge, object_of_class=edge
        )
        await element.delete_element_from_db()


async def get_edges_of_nodes(nodes: list) -> list[Edge]:
    edges = []
    for node in nodes:
        edges_found = await get_edges_of_node(node=node)
        edges.extend(edges_found)
    unique_edges_list = list(set(edges))
    return unique_edges_list
