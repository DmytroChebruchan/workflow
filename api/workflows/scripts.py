import networkx as nx
from matplotlib import pyplot as plt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from api.nodes.node_attr_values import NodeType
from api.nodes.schemas.schemas_by_nodes_creating_stage import NodeCreate
from api.nodes.scripts import (
    create_node_script,
    delete_nodes_of_workflow_script,
)
from api.workflows.crud_WorkflowRepo import WorkflowRepo
from api.workflows.schemas import WorkflowCreate, WorkflowUpdate
from core.graph.script import creating_graph_script


async def create_workflow_with_nodes_script(
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


async def update_workflow_script(
    session, workflow_id: int, workflow_update: WorkflowUpdate
):
    workflow_object = WorkflowRepo(session=session, workflow_id=workflow_id)
    workflow = await workflow_object.get_workflow_by_id()
    await workflow_object.update_workflow(
        workflow_update=workflow_update,
        workflow=workflow,
    )

    return Response(
        content=f"Workflow with id {str(workflow_id)} was updated.",
        status_code=200,
    )


async def run_workflow_script(session: AsyncSession, workflow_id: int) -> dict:
    """
    Run a workflow.

    Args:
        session (AsyncSession): Async session for database operations.
        workflow_id (int): ID of the workflow to run.

    Returns:
        dict: Path details of the executed workflow.
    """
    # Get workflow by ID
    workflow_object = WorkflowRepo(session=session, workflow_id=workflow_id)
    workflow = await workflow_object.get_workflow_by_id()

    # Collect nodes from the workflow
    graph = await creating_graph_script(session, workflow)

    # Return path details of the executed workflow
    return await graph.find_path()


async def delete_workflow_script(
    session: AsyncSession, workflow_id: int
) -> Response:
    await delete_nodes_of_workflow_script(
        session=session, workflow_id=workflow_id
    )
    workflow_object = WorkflowRepo(session=session, workflow_id=workflow_id)
    await workflow_object.delete_workflow_by_id()
    return Response(
        content=f"Workflow with id {str(workflow_id)} was deleted.",
        media_type="text/plain",
        status_code=200,
    )
