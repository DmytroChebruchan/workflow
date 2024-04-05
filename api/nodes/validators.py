from fastapi import HTTPException
from starlette import status

from api.nodes.schemas import NodeCreate, NodeUpdate
from api.nodes.node_attr_values import NodeType
from core.models import Node, Workflow


async def validate_node_type(node_in: NodeCreate | NodeUpdate) -> None:
    if node_in.type not in NodeType:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid node type provided",
        )


async def validate_status(node_in: NodeCreate | NodeUpdate) -> None:
    if node_in.type != NodeType.MESSAGE and node_in.status is not None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Status can be provided only for nodes with 'Message Node' type",
        )


async def validate_message(node_in: NodeCreate | NodeUpdate) -> None:
    if node_in.type != NodeType.MESSAGE and node_in.message_text is not None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Message text can be provided only for nodes with 'Message Node' type",
        )


async def validate_existence_of_node(node: Node) -> None:
    if node is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Node with ID {node.id} not found",
        )


async def validate_existence_of_workflow(
    node_update: NodeCreate | NodeUpdate,
) -> None:
    workflow_id = node_update.workflow_id
    workflow = Workflow.get_by_id(workflow_id)
    if workflow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow with ID {workflow_id} not found",
        )


async def validate_node_for_update(node_update: NodeUpdate) -> None:
    await validate_node_type(node_update)
    await validate_status(node_update)
    await validate_message(node_update)
    await validate_existence_of_workflow(node_update)
