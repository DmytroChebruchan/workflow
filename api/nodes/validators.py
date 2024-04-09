from typing import Union

from fastapi import HTTPException
from starlette import status

from api.nodes.node_attr_values import NodeType
from api.nodes.schemas import NodeCreate, NodeUpdate
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


async def validate_condition_of_node(node_in: NodeCreate | NodeUpdate) -> None:
    if node_in.condition and node_in.type != NodeType.CONDITION:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Condition can be provided only for nodes with 'Condition Node' type",
        )


async def validate_existence_of_node(node: Node) -> None:
    if node is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Node with ID {node.id} not found",
        )


async def validate_condition_node(node: Union[NodeUpdate, NodeCreate]) -> None:
    if node.type == NodeType.CONDITION and node.condition is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Condition Node cannot be created without condition.",
        )
    if node.type != NodeType.CONDITION and node.condition is not None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Only Condition Nodes can have condition.",
        )


async def validate_node(node: Union[NodeUpdate, NodeCreate]) -> None:
    await validate_node_type(node)
    await validate_status(node)
    await validate_message(node)
    await validate_condition_of_node(node)
    await validate_condition_node(node)
