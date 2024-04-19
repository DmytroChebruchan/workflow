from sqlalchemy.ext.asyncio import AsyncSession

from api.nodes.crud import create_node
from api.nodes.schemas.schemas import NodeCreate
from api.workflows.crud import create_workflow
from api.workflows.schemas import WorkflowCreate


async def create_workflow_with_nodes(
    session: AsyncSession, workflow_in: WorkflowCreate
):

    workflow = await create_workflow(session, workflow_in)

    # creating start and end nodes
    start_node_info = NodeCreate(workflow_id=workflow.id, type="Start Node")
    created_start_node = await create_node(
        session=session, node_in=start_node_info
    )

    end_node_info = NodeCreate(
        workflow_id=workflow.id,
        type="End Node",
        from_node_id=created_start_node.id,
    )
    await create_node(session=session, node_in=end_node_info)

    return workflow
