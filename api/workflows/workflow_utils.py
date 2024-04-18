from sqlalchemy.ext.asyncio import AsyncSession

from api.workflows.schemas import WorkflowCreate
from core.models.node import Node
from core.models.workflow import Workflow


async def create_workflow_with_nodes(
    session: AsyncSession, workflow_in: WorkflowCreate
):

    workflow = Workflow(**workflow_in.model_dump())
    session.add(workflow)
    await session.commit()
    await session.refresh(workflow)

    return workflow
