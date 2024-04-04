from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.workflows.schemas import WorkflowCreate
from core.models import Workflow


async def get_workflows(session: AsyncSession) -> list[Workflow]:
    stmt = select(Workflow).order_by(Workflow.id)
    result: Result = await session.execute(stmt)
    workflows = result.scalars().all()
    return list(workflows)


async def get_workflow_by_id(
    session: AsyncSession, workflow_id: int
) -> Workflow | None:
    return await session.get(Workflow, workflow_id)


async def create_workflow(
    session: AsyncSession, workflow_in: WorkflowCreate
) -> Workflow:
    workflow = Workflow(**workflow_in.model_dump())
    session.add(workflow)
    await session.commit()
    await session.refresh(workflow)
    return workflow
