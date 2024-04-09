from typing import Union

from fastapi import HTTPException
from starlette import status

from api.nodes.node_attr_values import MessageNodeStatus, NodeType
from api.nodes.schemas.schemas import NodeCreate, NodeUpdate
from core.models import Node


async def validate_existence_of_node(node: Node) -> None:
    if node is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Node with ID {node.id} not found",
        )
