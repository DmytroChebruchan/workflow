from sqlalchemy.ext.asyncio import AsyncSession

from api.nodes.node_attr_values import NodeType
from api.nodes.schemas.schemas_by_nodes_creating_stage import NodeCreate
from api.nodes.scripts import create_node_script
from api.workflows.crud_WorkflowRepo import WorkflowRepo
from api.workflows.schemas import WorkflowCreate


async def create_workflow_with_nodes(
    session: AsyncSession, workflow_in: WorkflowCreate
):
    workflow_object = WorkflowRepo(session=session)
    workflow = await workflow_object.create_workflow(workflow_in=workflow_in)

    # creating start and end nodes
    start_node_info = NodeCreate(workflow_id=workflow.id, type=NodeType.START)
    created_start_node = await create_node_script(
        session=session, node_in=start_node_info
    )

    end_node_info = NodeCreate(
        workflow_id=workflow.id,
        type=NodeType.END,
        from_node_id=created_start_node.id,
        edge_condition_type=True,
    )
    await create_node_script(session=session, node_in=end_node_info)

    return workflow
