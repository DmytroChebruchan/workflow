from sqlalchemy.ext.asyncio import AsyncSession

from api.nodes.validation.utils import nodes_validation_by_id
from api.nodes.validation.validation_with_pydentic import (
    condition_node_validation,
    node_type_validation,
    node_validation_according_to_type,
)
from core.models import Node


async def nodes_val_with_pydentic_script(
    data: dict, session: AsyncSession
) -> None:
    await node_type_validation(data["type"])
    await node_validation_according_to_type(data, data["type"])
    await condition_node_validation(data=data, session=session)
    await nodes_validation_by_id(
        session=session,
        data=data,
        element=Node,
    )
