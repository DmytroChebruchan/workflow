from fastapi import HTTPException
from starlette import status

from api.nodes.schemas_node_by_type import NODE_TYPE_TO_SCHEMA


async def nodes_validation_with_pydentic(data: dict) -> None:
    await node_type_validation(data["type"])
    await node_validation_according_to_type(data, data["type"])


async def node_validation_according_to_type(data: dict, node_type) -> None:
    try:
        schema = NODE_TYPE_TO_SCHEMA[node_type]
        schema(**data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to validate node of type {node_type}: {e}",
        )


async def node_type_validation(node_type) -> None:
    if node_type not in NODE_TYPE_TO_SCHEMA:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid node type: {node_type}",
        )
