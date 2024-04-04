from sqlalchemy.orm import Session

from api.models.schemas import NodeBase


def create_new_node(node_in: NodeBase) -> dict:
    node = node_in.model_dump()
    return {"success": True,
            "node": node}