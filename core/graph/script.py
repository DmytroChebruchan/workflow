from api.general.utils import get_edges_of_nodes
from core.graph.workflow_graph import WorkflowGraph


async def creating_graph_script(session, workflow):
    nodes = list(workflow.nodes)
    # Get edges between nodes
    edges = await get_edges_of_nodes(nodes)
    # Create a workflow graph
    graph = WorkflowGraph(
        nodes=nodes,
        edges=edges,
        session=session,
    )
    return graph
