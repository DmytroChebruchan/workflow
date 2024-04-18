from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import get_element_by_id
from api.workflows.schemas import WorkflowCreate, WorkflowUpdate
from core.models.workflow import Workflow


async def get_workflow_by_id(
    session: AsyncSession, workflow_id: int
) -> Workflow | None:
    return await get_element_by_id(
        element=Workflow,
        session=session,
        element_id=workflow_id,
    )


async def update_workflow(
    session: AsyncSession,
    workflow_update: WorkflowUpdate,
    workflow,
) -> Workflow | None:

    for field, value in workflow_update.dict(exclude_unset=True).items():
        setattr(workflow, field, value)

    await session.commit()
    await session.refresh(workflow)
    return workflow


async def delete_workflow_by_id(
    session: AsyncSession, workflow: Workflow
) -> dict[str, str]:
    await session.delete(workflow)
    await session.commit()
    return {"details": "Workflow deleted"}
