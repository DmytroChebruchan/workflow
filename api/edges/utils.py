from _operator import and_
from sqlalchemy import and_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Edge


async def delete_destination_edge(
    node_from_id: int, successors_nodes: dict, session: AsyncSession
):
    successors_nodes_ids = [node_to for node_to in successors_nodes.values()]
    # Delete edges that match the conditions
    await session.execute(
        delete(Edge).where(
            and_(
                Edge.source_node_id == node_from_id,
                Edge.destination_node_id.in_(successors_nodes_ids),
            )
        )
    )


async def delete_edge_from_source(
    edge_condition_type: bool, node_from_id: int, session: AsyncSession
):
    await session.execute(
        delete(Edge).where(
            and_(
                Edge.source_node_id == node_from_id,
                Edge.condition_type == edge_condition_type,
            )
        )
    )


async def delete_successors_connecting_edge(
    session: AsyncSession, nodes: dict
):
    true_node_id = nodes[True]
    false_node_id = nodes[False]

    # Delete edges connecting true_node_id to false_node_id
    await session.execute(
        delete(Edge).where(
            and_(
                Edge.source_node_id == true_node_id,
                Edge.destination_node_id == false_node_id,
            )
        )
    )

    # Delete edges connecting false_node_id to true_node_id
    await session.execute(
        delete(Edge).where(
            and_(
                Edge.source_node_id == false_node_id,
                Edge.destination_node_id == true_node_id,
            )
        )
    )
