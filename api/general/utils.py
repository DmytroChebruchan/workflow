from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.general.validators import element_validator


async def get_elements(session: AsyncSession, element) -> list:
    stmt = select(element).order_by(element.id)
    result: Result = await session.execute(stmt)
    nodes = result.scalars().all()
    return list(nodes)


async def get_element_by_id(session: AsyncSession, element_id: int, element):
    item = await session.get(element, element_id)
    await element_validator(element_id=element_id, item=item)
    return item


async def save_element_into_db(session: AsyncSession, element):
    session.add(element)
    await commit_and_refresh_element(session=session, element=element)
    return element


async def delete_element_from_db(session: AsyncSession, element):
    await session.delete(element)
    await session.commit()


async def commit_and_refresh_element(session: AsyncSession, element):
    await session.commit()
    await session.refresh(element)


async def update_element_id_checker(original_id: int, update_id: int):
    if original_id != update_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Workflow with ID {update_id} in "
            f"update workflow is not correct.",
        )
