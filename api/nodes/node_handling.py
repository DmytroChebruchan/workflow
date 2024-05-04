from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Node


async def get_nodes_by_type(
    session: AsyncSession, node_type: str, workflow_id: int
) -> list:
    stmt = select(Node).where(
        and_(Node.type == node_type, Node.workflow_id == workflow_id)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def delete_nodes_of_workflow(
    session: AsyncSession, workflow_id: int
) -> None:
    await session.execute(delete(Node).where(Node.workflow_id == workflow_id))
    await session.commit()
