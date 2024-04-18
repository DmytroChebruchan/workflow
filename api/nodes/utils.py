from api.edge.crud import create_edge
from api.nodes.schemas.schemas import NodeCreate
from core.models import Node


async def creating_required_edges(
    node: Node, node_in: NodeCreate, session
) -> None:
    if node_in.from_node_id:
        await create_edge(
            from_node_id=node_in.from_node_id,
            to_node_id=node.id,
            session=session,
        )
    if node_in.to_node_id:
        await create_edge(
            from_node_id=node.id, to_node_id=node_in.to_node_id, session=session
        )


async def node_model_dict_generator(node_in):
    keys_to_exclude = ["from_node_id", "to_node_id"]
    node_model_dict = {
        key: value
        for key, value in node_in.model_dump().items()
        if key not in keys_to_exclude
    }
    return node_model_dict


async def node_saver(node_model_dict, session):
    node = Node(**node_model_dict)
    session.add(node)
    await session.commit()
    await session.refresh(node)
    return node