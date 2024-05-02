from typing import List

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def nodes_validation_by_id(session: AsyncSession, data: dict, element):
    ids = await ids_of_nodes_related(data)
    if not ids:
        return
    nodes = await get_elements_by_ids(
        session=session, ids=ids, element=element
    )
    if len(nodes) != len(ids):
        raise ValidationError("Nodes related are not valid.")


async def ids_of_nodes_related(data) -> list:
    nodes_ids = [data["from_node_id"]]
    if nodes_ids[0] is None or data["nodes_dest_dict"] is None:
        return []
    for key in data["nodes_dest_dict"]:
        nodes_ids.append(data["nodes_dest_dict"][key])
    return nodes_ids


async def get_elements_by_ids(session: AsyncSession, ids: List[int], element):
    # Query to fetch all elements with IDs in the input list
    query = select(element).where(element.id.in_(ids))

    # Fetch all elements with the query
    result = await session.execute(query)
    elements = result.scalars().all()

    return elements
