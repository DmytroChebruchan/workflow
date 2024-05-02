from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.nodes.node_attr_values import NodeType
from api.nodes.node_handling import get_nodes_by_type
from api.nodes.schemas.schemas import NodeCreate
from api.workflows.crud_WorkflowManagement import WorkflowManagement


async def check_node_type_existence_in_workflow(
    node_in: NodeCreate, session: AsyncSession
) -> None:

    # collecting values fot check
    workflow_id = node_in.workflow_id
    workflow_object = WorkflowManagement(
        session=session, workflow_id=workflow_id
    )
    await workflow_object.get_workflow_by_id()
    node_type = node_in.type

    # checker
    await ensure_unique_node_type(
        node_type=node_type,
        workflow_id=workflow_id,
        session=session,
    )


async def ensure_unique_node_type(
    node_type: str, workflow_id: int, session: AsyncSession
):
    if node_type != NodeType.START and node_type != NodeType.END:
        return

    nodes_of_type = await get_nodes_by_type(
        session, node_type=node_type, workflow_id=workflow_id
    )

    if nodes_of_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Workflow with ID {workflow_id} has a {node_type}",
        )
