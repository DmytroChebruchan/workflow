from sqlalchemy import and_, delete

from core.models import Edge


async def del_destination_edge(node_from_id, nodes_destination, session):
    destination_node_ids = [node_to for node_to in nodes_destination.values()]
    # Delete edges that match the conditions
    await session.execute(
        delete(Edge).where(
            (Edge.source_node_id == node_from_id)
            and (Edge.destination_node_id.in_(destination_node_ids))
        )
    )


async def delete_edge_from_source(edge_condition_type, node_from_id, session):
    await session.execute(
        delete(Edge).where(
            and_(
                Edge.source_node_id == node_from_id,
                Edge.condition_type == edge_condition_type,
            )
        )
    )
