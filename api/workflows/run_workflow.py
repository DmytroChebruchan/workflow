from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import select

from core.models.workflow import Workflow


async def run_workflow(session: AsyncSession, workflow_id: int) -> dict | None:
    # get workflow
    result = await session.execute(
        select(Workflow)
        .where(Workflow.id == workflow_id)
        .options(selectinload(Workflow.nodes))
    )
    workflow = result.scalars().first()

    # get nodes
    if not workflow:
        return None

    nodes = [
        {
            "id": node.id,
            "type": node.type,
            "status": node.status,
            "message_text": node.message_text,
        }
        for node in workflow.nodes
    ]
    # get edges
    # create_graph
    # generate reply
    return {"id": workflow.id, "title": workflow.title, "nodes": nodes}
