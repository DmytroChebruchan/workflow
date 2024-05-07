from core.models import Node


async def edge_step_generator(edge, steps):
    steps.append(
        {
            "type": "edge",
            "value": {"condition_of_edge": edge["condition"]},
        }
    )


async def node_step_generator(node: Node, steps: list):
    node_dict = await node_dict_generator(node)
    steps.append({"type": "node", "value": node_dict})


async def node_dict_generator(node: Node):
    node_dict = {"type": node.type}
    if node.type == "Condition Node":
        node_dict["condition"] = node.condition
    if node.type == "Message Node":
        node_dict["message"] = node.message_text
        node_dict["status"] = node.status
    return node_dict
