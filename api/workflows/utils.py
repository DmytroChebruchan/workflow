from typing import List

from core.models import Workflow


async def get_nodes_of_workflow(workflow: Workflow) -> List[dict]:
    nodes = [
        {
            "id": node.id,
            "type": node.type,
            "status": node.status,
            "message_text": node.message_text,
        }
        for node in workflow.nodes
    ]
    return nodes
