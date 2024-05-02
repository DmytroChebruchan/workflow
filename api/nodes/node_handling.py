from sqlalchemy import Result, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils_element_class import ElementManagement
from core.models import Edge, Node


async def get_edges_of_node(node: Node) -> list[Edge]:
    outgoing_edges = list(node.outgoing_edges)
    incoming_edges = list(node.incoming_edges)
    unique_edges = set(outgoing_edges + incoming_edges)
    return list(unique_edges)


async def delete_edges_of_node(node: Node, session: AsyncSession) -> None:
    edges_related = await get_edges_of_node(node=node)
    for edge in edges_related:
        element = ElementManagement(
            session=session, model=Edge, class_object=edge
        )
        await element.delete_element_from_db()


async def get_edges_of_nodes(nodes: list) -> list[Edge]:
    edges = []
    for node in nodes:
        edges_found = await get_edges_of_node(node=node)
        edges.extend(edges_found)
    unique_edges_list = list(set(edges))
    return unique_edges_list


async def get_nodes_by_type(
    session: AsyncSession, node_type: str, workflow_id: int
) -> list:
    stmt = select(Node).where(
        and_(Node.type == node_type, Node.workflow_id == workflow_id)
    )
    result: Result = await session.execute(stmt)
    return list(result.scalars().all())
