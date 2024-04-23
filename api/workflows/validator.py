from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.nodes.node_attr_values import NodeType
from api.workflows.crud import get_workflow_by_id
from core.models import Node


async def check_node_type_existence_in_workflow(
    node_model_dict: dict, session: AsyncSession
) -> None:

    # collecting values fot check
    workflow_id = node_model_dict["workflow_id"]
    workflow = await get_workflow_by_id(
        workflow_id=workflow_id, session=session
    )
    node_type = node_model_dict["type"]

    # checker
    await nodes_existing_checker(
        node_type=node_type,
        workflow=workflow,
        session=session,
    )


async def nodes_existing_checker(node_type, workflow, session: AsyncSession):
    if (
        node_type == NodeType.START
        and session.query(Node)
        .filter(Node.workflow == workflow, Node.type == NodeType.START)
        .first()
        is not None
    ) or (
        node_type == NodeType.END
        and session.query(Node)
        .filter(Node.workflow == workflow, Node.type == NodeType.END)
        .first()
        is not None
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Workflow with ID {workflow.id} has a {node_type}",
        )
