from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Workflow

from sqlalchemy.orm import selectinload
from sqlalchemy.sql import select


async def run_workflow(session: AsyncSession, workflow_id: int) -> dict | None:
    result = await session.execute(
        select(Workflow)
        .where(Workflow.id == workflow_id)
        .options(selectinload(Workflow.nodes))
    )
    workflow = result.scalars().first()
    if workflow:
        nodes = [
            {
                "id": node.id,
                "type": node.type,
                "status": node.status,
                "message_text": node.message_text,
            }
            for node in workflow.nodes
        ]
        return {"id": workflow.id, "title": workflow.title, "nodes": nodes}
    return None
