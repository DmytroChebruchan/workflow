from sqlalchemy.ext.asyncio import AsyncSession

from api.nodes.node_handling import get_edges_of_nodes
from api.workflows.crud import get_workflow_by_id
from core.graph.workflow_graph import WorkflowGraph


async def run_workflow(session: AsyncSession, workflow_id: int) -> dict:
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
