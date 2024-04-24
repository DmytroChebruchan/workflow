from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.nodes.node_attr_values import NodeType
from api.nodes.node_handling import get_nodes_by_type

from api.workflows.crud import get_workflow_by_id


async def check_node_type_existence_in_workflow(
    node_model_dict: dict, session: AsyncSession
) -> None:

    # collecting values fot check
    workflow_id = node_model_dict["workflow_id"]
    await get_workflow_by_id(workflow_id=workflow_id, session=session)
    node_type = node_model_dict["type"]

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

    if nodes_of_type is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Workflow with ID {workflow_id} has a {node_type}",
        )
