from sqlalchemy.ext.asyncio import AsyncSession

from api.nodes.validation.validation_with_pydentic import (
    node_type_validation,
    node_validation_according_to_type,
    condition_node_validation,
)


async def nodes_val_with_pydentic_script(
    data: dict, session: AsyncSession
) -> None:
    await node_type_validation(data["type"])
    await node_validation_according_to_type(data, data["type"])
    await condition_node_validation(data=data, session=session)
