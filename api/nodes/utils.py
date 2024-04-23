from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import (
    delete_element_from_db,
    save_element_into_db,
)
from api.nodes.node_attr_values import NodeType
from api.workflows.validator import check_node_type_existence_in_workflow
from core.models import Edge, Node


async def node_model_dict_generator(node_in) -> dict:
    keys_to_exclude = ["from_node_id", "nodes_to_list"]
    node_model_dict = {
        key: value
        for key, value in node_in.model_dump().items()
        if key not in keys_to_exclude
    }
    return node_model_dict


async def node_saver(node_model_dict: dict, session: AsyncSession) -> Node:
    await check_node_type_existence_in_workflow(
        node_model_dict=node_model_dict, session=session
    )
    node = Node(**node_model_dict)
    return await save_element_into_db(session=session, element=node)


async def get_edges_of_node(node: Node) -> list[Edge]:
    outgoing_edges = list(node.outgoing_edges)
    incoming_edges = list(node.incoming_edges)
    unique_edges = set(outgoing_edges + incoming_edges)
    return list(unique_edges)


async def delete_edges_of_node(node: Node, session: AsyncSession) -> None:
    edges_related = await get_edges_of_node(node=node)
    for edge in edges_related:
        await delete_element_from_db(session=session, element=edge)


async def get_edges_of_nodes(nodes: list, session: AsyncSession) -> list[Edge]:
    edges = []
    for node in nodes:
        edges_found = await get_edges_of_node(node=node, session=session)
        edges.extend(edges_found)
    unique_edges_list = list(set(edges))
    return unique_edges_list


async def find_node_by_type(nodes: list, node_type: NodeType) -> Node | None:
    return next((node for node in nodes if node.type == node_type), None)
