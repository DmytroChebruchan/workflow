from unittest.mock import Mock

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


async def message_mock_returner(*args, **kwargs):
    node_mock = Mock()
    node_mock.type = "Message Node"
    return node_mock


async def start_node_mock_returner(*args, **kwargs):
    node_mock = Mock()
    node_mock.type = "Start Node"
    return node_mock
