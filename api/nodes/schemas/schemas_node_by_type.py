from typing import Optional

from pydantic import BaseModel, ConfigDict

from api.nodes.node_attr_values import MessageNodeStatus, NodeType
from api.nodes.schemas.schemas import NodeBase


class StartNode(NodeBase):
    node_type: NodeType.START


class MessageNode(NodeBase):
    node_type: NodeType.MESSAGE
    message: str
    status: MessageNodeStatus


class ConditionNode(NodeBase):
    node_type: NodeType.CONDITION
    condition: str

    id_of_true_condition: int
    id_of_false_condition: int
