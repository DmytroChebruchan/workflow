from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import save_element_into_db
from api.nodes.schemas.schemas import NodeCreate
from api.nodes.validators import node_validator
from core.models import Node
from core.models.edge import Edge


async def create_edge(
    from_node_id: int,
    to_node_id: int,
    session: AsyncSession,
    condition: Optional[bool] = True,
) -> Edge:

    # Retrieve source and destination nodes
    await node_validator(from_node_id, session)
    await node_validator(to_node_id, session)

    # Create and persist the edges
    edge = Edge(
        source_node_id=from_node_id,
        destination_node_id=to_node_id,
        condition_type=condition,
    )
    return await save_element_into_db(session=session, element=edge)


async def creating_required_edges(
    node: Node, node_in: NodeCreate, session
) -> None:
    if node_in.from_node_id:
        await create_edge(
            from_node_id=node_in.from_node_id,
            to_node_id=node.id,
            session=session,
        )

    if node_in.nodes_to_list:
        for node_to in node_in.nodes_to_list:
            await create_edge(
                from_node_id=node_in.from_node_id,
                to_node_id=node_to["id"],
                session=session,
                condition=node_to["condition"],
            )
