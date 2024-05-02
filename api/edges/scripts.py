from sqlalchemy.ext.asyncio import AsyncSession

from api.edges.crud import creating_required_edges
from api.general.utils import get_element_by_id, save_element_into_db
from core.models import Edge, Node


async def create_edge_script(
    condition: bool, from_node_id: int, session: AsyncSession, to_node_id: int
):
    await get_element_by_id(
        session=session,
        element_id=from_node_id,
        element=Node,
    )
    await get_element_by_id(
        session=session,
        element_id=to_node_id,
        element=Node,
    )
    # Create and persist the edges
    edge = Edge(
        source_node_id=from_node_id,
        destination_node_id=to_node_id,
        condition_type=condition,
    )
    return await save_element_into_db(session=session, element=edge)


async def edge_creator_script(node, node_in, session) -> None:
    from_node_avail = node_in.from_node_id
    dest_node_avail = node_in.nodes_dest_dict
    if from_node_avail or dest_node_avail:
        await creating_required_edges(
            node_id=node.id,
            node_from_id=node_in.from_node_id,
            nodes_destination_dict=node_in.nodes_dest_dict,
            session=session,
        )
