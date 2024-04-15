from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select


async def get_elements(session: AsyncSession, element) -> list:
    stmt = select(element).order_by(element.id)
    result: Result = await session.execute(stmt)
    nodes = result.scalars().all()
    return list(nodes)


async def get_element_by_id(session: AsyncSession, element_id: int, element):
    return await session.get(element, element_id)
