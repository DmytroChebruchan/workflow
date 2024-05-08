message_node_1 = {
    "type": "Message Node",
    "workflow_id": "1",
    "from_node_id": "1",
    "nodes_dest_dict": {"true": "2"},
    "edge_condition_type": "true",
    "message_text": "Hello",
    "status": "opened",
}

message_node_2 = {
    "type": "Message Node",
    "workflow_id": "1",
    "from_node_id": "3",
    "nodes_dest_dict": {"true": "2"},
    "edge_condition_type": "true",
    "message_text": "How are you?",
    "status": "pending",
}

message_node_3 = {
    "type": "Message Node",
    "workflow_id": "1",
    "from_node_id": "4",
    "nodes_dest_dict": {"true": "2"},
    "edge_condition_type": "true",
    "message_text": "How old are you?",
    "status": "pending",
}

message_node_4 = {
    "type": "Message Node",
    "workflow_id": "1",
    "from_node_id": "5",
    "nodes_dest_dict": {"true": "2"},
    "edge_condition_type": "true",
    "message_text": "Do you like pets?",
    "status": "pending",
}

condition_node_1 = {
    "type": "Condition Node",
    "workflow_id": "1",
    "from_node_id": "3",
    "nodes_dest_dict": {"true": "4", "false": "5"},
    "edge_condition_type": "true",
    "condition": "sent",
}

condition_node_2 = {
    "type": "Condition Node",
    "workflow_id": "1",
    "from_node_id": "7",
    "nodes_dest_dict": {"true": "5", "false": "6"},
    "edge_condition_type": "false",
    "condition": "opened",
}

nodes_to_create = [
    message_node_1,
    message_node_2,
    message_node_3,
    message_node_4,
    condition_node_1,
    condition_node_2,
]

message_node_2_update = {
    "id": 4,
    "type": "Message Node",
    "workflow_id": "1",
    "from_node_id": "7",
    "nodes_dest_dict": {"true": "2"},
    "edge_condition_type": "true",
    "message_text": "How are you?",
    "status": "pending",
}

message_node_3_update = {
    "id": 5,
    "type": "Message Node",
    "workflow_id": "1",
    "from_node_id": "8",
    "nodes_dest_dict": {"true": "2"},
    "edge_condition_type": "true",
    "message_text": "How old are you?",
    "status": "pending",
}

nodes_to_update = [message_node_2_update, message_node_3_update]
