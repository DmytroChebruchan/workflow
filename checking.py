import asyncio

from sqlalchemy import Column, Result, String, literal_column, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Node


async def get_node_by_type(session: AsyncSession, node_type: str) -> list:
    stmt = select(Node).where(Node.type == literal_column(node_type))
    result: Result = await session.execute(stmt)
    nodes = result.scalars().all()
    print(list(nodes))


if __name__ == "__main__":
    asyncio.run(
        get_node_by_type(node_type="Start Node", session=AsyncSession())
    )
