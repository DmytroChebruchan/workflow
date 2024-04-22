from sqlalchemy.ext.asyncio import AsyncSession

from api.nodes.utils import get_edges_of_nodes
from api.workflows.crud import get_workflow_by_id
from core.graph.utils import get_path, workflow_graph_checker


async def run_workflow(session: AsyncSession, workflow_id: int) -> dict | None:
    # get workflow
    workflow = await get_workflow_by_id(
        workflow_id=workflow_id,
        session=session,
    )
    if not workflow:
        return None

    # get nodes
    # nodes = await get_nodes_of_workflow(workflow)
    nodes = list(workflow.nodes)
    # get edges
    edges = await get_edges_of_nodes(nodes, session)
    # create_graph
    reply = {
        "connection_between_start_and_finish": await workflow_graph_checker(
            nodes=nodes, edges=edges, session=session
        ),
        "path": await get_path(nodes=nodes, edges=edges, session=session),
    }
    # generate reply
    return reply
