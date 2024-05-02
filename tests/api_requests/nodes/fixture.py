dummy_msg_node = {
    "type": "Message Node",
    "workflow_id": 1,
    "message_text": "Hello World",
    "status": "pending",
    "from_node_id": 22,
    "edge_condition_type": True,
    "nodes_dest_dict": {True: 4},
}

expected_data = {
    "type": "Message Node",
    "workflow_id": 1,
    "message_text": "Hello World",
    "status": "pending",
    "id": 1,
    "condition": None,
}
