from starlette.responses import Response

from api.nodes.script import delete_nodes_of_workflow_script
from api.workflows.crud import (
    delete_workflow_by_id,
    get_workflow_by_id,
    update_workflow,
)
from api.workflows.run_workflow import run_workflow
from api.workflows.schemas import WorkflowUpdate


async def run_workflow_script(session, workflow_id):
    await get_workflow_by_id(session=session, workflow_id=workflow_id)
    return await run_workflow(session=session, workflow_id=workflow_id)


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
