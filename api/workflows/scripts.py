from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from api.nodes.node_handling import get_edges_of_nodes
from api.nodes.script import delete_nodes_of_workflow_script
from api.workflows.crud import (
    delete_workflow_by_id,
    get_workflow_by_id,
    update_workflow,
)
from api.workflows.schemas import WorkflowUpdate
from core.graph.workflow_graph import WorkflowGraph


async def delete_workflow_script(session, workflow_id):
    await delete_nodes_of_workflow_script(
        session=session, workflow_id=workflow_id
    )
    await delete_workflow_by_id(session=session, workflow_id=workflow_id)
    return Response(
        content=f"Workflow with id {str(workflow_id)} was deleted.",
        media_type="text/plain",
        status_code=200,
    )


async def update_workflow_script(
    session, workflow_id: int, workflow_update: WorkflowUpdate
):
    workflow = await get_workflow_by_id(
        workflow_id=workflow_id, session=session
    )
    await update_workflow(
        session=session,
        workflow=workflow,
        workflow_update=workflow_update,
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
    workflow = await get_workflow_by_id(
        workflow_id=workflow_id,
        session=session,
    )

    # Collect nodes from the workflow
    nodes = list(workflow.nodes)

    # Get edges between nodes
    edges = await get_edges_of_nodes(nodes)

    # Create a workflow graph
    graph = WorkflowGraph(
        nodes=nodes,
        edges=edges,
        session=session,
    )

    # Update the graph asynchronously
    await graph.async_update_graph()

    # Return path details of the executed workflow
    return await graph.find_path()
