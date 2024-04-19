from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


async def get_elements(session: AsyncSession, element) -> list:
    stmt = select(element).order_by(element.id)
    result: Result = await session.execute(stmt)
    nodes = result.scalars().all()
    return list(nodes)


async def get_element_by_id(session: AsyncSession, element_id: int, element):
    return await session.get(element, element_id)


async def save_element_into_db(session: AsyncSession, element):
    session.add(element)
    await session.commit()
    await session.refresh(element)
    return element


async def delete_element_from_db(session: AsyncSession, element):
    await session.delete(element)
    await session.commit()
    await session.refresh(element)
    return element
