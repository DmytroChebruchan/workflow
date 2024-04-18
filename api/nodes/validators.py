from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.general.utils import get_element_by_id
from core.models.node import Node


async def validate_existence_of_node(node: Node) -> None:
    if node is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Node with ID {node.id} not found",
        )


async def node_validator(node_id: int, session: AsyncSession) -> Node:
    node = await get_element_by_id(
        session=session,
        element_id=node_id,
        element=Node,
    )
    await validate_existence_of_node(node)
    return node
