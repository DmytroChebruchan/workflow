from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.nodes.schemas import NodeCreate
from core.models import Node


async def get_nodes(session: AsyncSession) -> list[Node]:
    stmt = select(Node).order_by(Node.id)
    result: Result = await session.execute(stmt)
    nodes = result.scalars().all()
    return list(nodes)


async def get_node_by_id(
        session: AsyncSession, node_id: int
) -> Node | None:
    return await session.get(Node, node_id)


async def create_node(
        session: AsyncSession, node_in: NodeCreate
) -> Node:
    node = Node(**node_in.model_dump())
    session.add(node)
    await session.commit()
    await session.refresh(node)
    return node


async def delete_node_by_id(session: AsyncSession, node_id: int) -> None:
    node = await get_node_by_id(session, node_id)
    if node:
        await session.delete(node)
        await session.commit()
        await session.refresh(node)
