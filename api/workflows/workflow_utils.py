from sqlalchemy.ext.asyncio import AsyncSession
from api.workflows.schemas import WorkflowCreate
from core.models.node import Node
from core.models.workflow import Workflow


async def create_workflow_with_nodes(
    session: AsyncSession, workflow_in: WorkflowCreate
):

    workflow = Workflow(**workflow_in.model_dump())
    session.add(workflow)
    await session.flush()

    # Create the end node and add it to the workflow
    end_node = Node(type="End Node", workflow_id=workflow.id)
    session.add(end_node)
    await session.flush()
    await session.refresh(end_node)

    # Create the start node and add it to the workflow
    start_node = Node(
        type="Start Node",
        workflow_id=workflow.id,
        id_of_true_condition=end_node.id,
    )
    session.add(start_node)
    await session.flush()

    return workflow
