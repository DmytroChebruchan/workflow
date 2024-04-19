from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import save_element_into_db, delete_element_from_db
from core.models import Node, Edge


async def node_model_dict_generator(node_in) -> dict:
    keys_to_exclude = ["from_node_id", "nodes_to_list"]
    node_model_dict = {
        key: value
        for key, value in node_in.model_dump().items()
        if key not in keys_to_exclude
    }
    return node_model_dict


async def node_saver(node_model_dict, session) -> Node:
    node = Node(**node_model_dict)
    return await save_element_into_db(session=session, element=node)


async def get_edges_of_node(node: Node, session: AsyncSession) -> list[Edge]:
    edges_query = await session.execute(
        select(Edge).filter(
            Edge.source_node == node.id or Edge.destination_node == node.id
        )
    )
    edges = edges_query.scalars().all()
    return list(edges)


async def delete_edges_related(node: Node, session: AsyncSession) -> None:
    edges_related = await get_edges_of_node(node=node, session=session)
    for edge in edges_related:
        await delete_element_from_db(session=session, element=edge)
