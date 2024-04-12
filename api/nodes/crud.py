from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.nodes.schemas.schemas import NodeCreate, NodeUpdate
from api.nodes.validation_with_pydentic import nodes_validation_with_pydentic
from api.nodes.validators import validate_existence_of_node
from core.models.node import Node


async def get_nodes(session: AsyncSession) -> list[Node]:
    stmt = select(Node).order_by(Node.id)
    result: Result = await session.execute(stmt)
    nodes = result.scalars().all()
    return list(nodes)


async def get_node_by_id(session: AsyncSession, node_id: int) -> Node | None:
    return await session.get(Node, node_id)


async def create_node(session: AsyncSession, node_in: NodeCreate) -> Node:
    node = await nodes_validation_with_pydentic(node_in.model_dump())
    session.add(node)
    await session.commit()
    await session.refresh(node)
    return node


async def delete_node_by_id(session: AsyncSession, node_id: int) -> None:
    node = await get_node_by_id(session=session, node_id=node_id)
    if node is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Node with ID {node_id} not found",
        )
    await session.delete(node)
    await session.commit()


async def update_node(
    session: AsyncSession, node_id: int, node_update: NodeUpdate
) -> Node:

    # Validate the updated node fields
    await nodes_validation_with_pydentic(node_update.model_dump())

    # Validate existence of node
    node = await get_node_by_id(session=session, node_id=node_id)
    await validate_existence_of_node(node)

    # Update the node fields
    for field, value in node_update.dict(exclude_unset=True).items():
        setattr(node, field, value)

    await session.commit()
    await session.refresh(node)
    return node
