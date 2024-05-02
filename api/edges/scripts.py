from api.edges.crud import creating_required_edges


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
