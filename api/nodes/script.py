from sqlalchemy.ext.asyncio import AsyncSession

from api.edges.crud import delete_edges_of_workflow
from api.nodes.crud import delete_nodes_of_workflow


async def delete_nodes_of_workflow_script(
    session: AsyncSession, workflow_id: int
) -> None:
    # Get the list of deleted node IDs
    await delete_edges_of_workflow(session=session, workflow_id=workflow_id)
    # Delete nodes of the specified workflow
    await delete_nodes_of_workflow(session=session, workflow_id=workflow_id)
