from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils_element_class import ElementManagement
from api.workflows.schemas import WorkflowCreate, WorkflowUpdate
from core.models.workflow import Workflow


async def create_workflow(session, workflow_in: WorkflowCreate) -> Workflow:
    workflow = Workflow(**workflow_in.model_dump())
    element = ElementManagement(
        session=session, model=Workflow, class_object=workflow
    )
    await element.save_element_into_db()
    return workflow


async def get_workflow_by_id(
    session: AsyncSession, workflow_id: int
) -> Workflow:
    element = ElementManagement(session=session, model=Workflow)
    return await element.get_element_by_id(
        element_id=workflow_id,
    )


async def update_workflow(
    session: AsyncSession,
    workflow_update: WorkflowUpdate,
    workflow: Workflow,
) -> Workflow:
    for field, value in workflow_update.model_dump(exclude_unset=True).items():
        setattr(workflow, field, value)
    element = ElementManagement(
        session=session, model=Workflow, class_object=workflow
    )
    await element.commit_and_refresh_element()
    return workflow


async def delete_workflow_by_id(
    session: AsyncSession, workflow_id: int
) -> None:
    workflow = await get_workflow_by_id(
        session=session, workflow_id=workflow_id
    )
    element = ElementManagement(
        session=session, model=Workflow, class_object=workflow
    )
    await element.delete_element_from_db()
