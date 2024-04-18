from api.general.utils import save_element_into_db
from core.models import Node


async def node_model_dict_generator(node_in) -> dict:
    keys_to_exclude = ["from_node_id", "to_node_id", "nodes_to_list"]
    node_model_dict = {
        key: value
        for key, value in node_in.model_dump().items()
        if key not in keys_to_exclude
    }
    return node_model_dict


async def node_saver(node_model_dict, session) -> Node:
    node = Node(**node_model_dict)
    return await save_element_into_db(session=session, element=node)
