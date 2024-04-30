from typing import Dict, Type

from api.nodes.schemas.schemas import NodeBase
from api.nodes.schemas.schemas_node_by_type import (
    ConditionNode,
    EndNode,
    MessageNode,
    StartNode,
)

NODE_TYPE_TO_SCHEMA: Dict[str, Type[NodeBase]] = {
    "Start Node": StartNode,
    "Message Node": MessageNode,
    "Condition Node": ConditionNode,
    "End Node": EndNode,
}
