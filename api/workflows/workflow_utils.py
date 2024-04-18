from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import save_element_into_db
from api.workflows.schemas import WorkflowCreate
from core.models.node import Node
from core.models.workflow import Workflow


async def create_workflow_with_nodes(
    session: AsyncSession, workflow_in: WorkflowCreate
):

    workflow = Workflow(**workflow_in.model_dump())
    await save_element_into_db(session=session, element=workflow)

    return workflow
