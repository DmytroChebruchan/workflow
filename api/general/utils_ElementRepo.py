from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.general.validators import element_validator


class ElementRepo:
    """
    This class is used to manage models. Get info from db, put in db.
    """

    def __init__(self, session: AsyncSession, model, object_of_class=None):
        self.session = session
        self.model = model
        self.object_of_class = object_of_class

    async def get_elements(self) -> list:
        stmt = select(self.model).order_by(self.model.id)
        result: Result = await self.session.execute(stmt)
        elements = result.scalars().all()
        return list(elements)

    async def get_element_by_id(self, element_id: int):
        item = await self.session.get(self.model, element_id)
        await element_validator(element_id=element_id, item=item)
        return item

    async def save_element_into_db(self):
        self.session.add(self.object_of_class)
        await self.commit_and_refresh_element()
        return self.object_of_class

    async def delete_element_from_db(self):
        await self.session.delete(self.object_of_class)
        await self.session.commit()

    async def commit_and_refresh_element(self):
        await self.session.commit()
        await self.session.refresh(self.object_of_class)
