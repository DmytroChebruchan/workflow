from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import save_element_into_db
from api.nodes.crud import create_node
from api.nodes.schemas.schemas import NodeCreate
from api.workflows.crud import create_workflow
from api.workflows.schemas import WorkflowCreate
from core.models import Node


async def create_workflow_with_nodes(
    session: AsyncSession, workflow_in: WorkflowCreate
):

    workflow = await create_workflow(session, workflow_in)

    # creating nodes with edges
    start_node = NodeCreate(workflow_id=workflow.id, type="Start Node")
    created_node = await create_node(session=session, node_in=start_node)

    end_node = NodeCreate(
        workflow_id=workflow.id,
        type="End Node",
        from_node_id=created_node.id,
    )
    end_node = await create_node(session=session, node_in=end_node)

    return workflow
