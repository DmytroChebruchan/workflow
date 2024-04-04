from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.nodes.schemas import NodeCreate
from api.nodes.validators import (
    validate_status,
    validate_node_type,
    validate_message,
)
from core.models import Node


async def get_nodes(session: AsyncSession) -> list[Node]:
    stmt = select(Node).order_by(Node.id)
    result: Result = await session.execute(stmt)
    nodes = result.scalars().all()
    return list(nodes)


async def get_node_by_id(session: AsyncSession, node_id: int) -> Node | None:
    return await session.get(Node, node_id)


async def create_node(session: AsyncSession, node_in: NodeCreate) -> Node:
    await validate_node_type(node_in)
    await validate_status(node_in)
    await validate_message(node_in)

    node = Node(**node_in.dict())
    session.add(node)
    await session.commit()
    await session.refresh(node)
    return node


async def delete_node_by_id(session: AsyncSession, node_id: int) -> None:
    node = await get_node_by_id(session=session, node_id=node_id)
    if node is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Node with ID {node_id} not found",
        )

    await session.delete(node)
    await session.commit()
