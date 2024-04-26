from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import save_element_into_db
from api.nodes.validator import check_node_type_existence_in_workflow
from core.models import Node


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
