from fastapi import HTTPException
from starlette import status

from api.nodes.schemas.schemas_node_by_type import (
    ConditionNode,
    EndNode,
    MessageNode,
    StartNode,
)
from core.models import Node

# Map node types to their corresponding Pydantic schemas
NODE_TYPE_TO_SCHEMA = {
    "Start Node": StartNode,
    "Message Node": MessageNode,
    "Condition Node": ConditionNode,
    "End Node": EndNode,
}


async def nodes_validation_with_pydentic(data: dict):
    node_type = data["type"]
    if node_type not in NODE_TYPE_TO_SCHEMA:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid node type: {node_type}",
        )

    try:
        schema = NODE_TYPE_TO_SCHEMA[node_type]
        node = schema(**data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to validate node of type {node_type}: {e}",
        )
    node = Node(**data)
    return node
