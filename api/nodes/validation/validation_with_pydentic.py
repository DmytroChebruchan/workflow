from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.general.utils_ElementRepo import ElementRepo
from api.nodes.node_attr_values import NodeType
from api.nodes.schemas.constants import NODE_TYPE_TO_SCHEMA
from core.models import Node


async def condition_node_validation(data: dict, session: AsyncSession):
    if data["type"] != NodeType.CONDITION:
        return

    element = ElementRepo(session=session, model=Node)
    node = await element.get_element_by_id(element_id=data["from_node_id"])

    if node.type in (NodeType.START, NodeType.END):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Condition node can be created only after "
            "Message Node or Condition Node.",
        )


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
