from fastapi import HTTPException
from starlette import status

from api.nodes.schemas import NodeCreate
from api.nodes.node_attr_values import NodeType


async def validate_node_type(node_in: NodeCreate) -> None:
    if node_in.type not in NodeType:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid node type provided",
        )


async def validate_status(node_in: NodeCreate) -> None:
    if node_in.type != NodeType.MESSAGE and node_in.status is not None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Status can be provided only for nodes with 'Message Node' type",
        )


async def validate_message(node_in: NodeCreate) -> None:
    if node_in.type != NodeType.MESSAGE and node_in.message_text is not None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Message text can be provided only for nodes with 'Message Node' type",
        )
