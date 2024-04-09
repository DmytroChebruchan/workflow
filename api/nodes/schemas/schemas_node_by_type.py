from pydantic.fields import Field

from api.nodes.node_attr_values import MessageNodeStatus, NodeType
from api.nodes.schemas.schemas import NodeBase


class StartNode(NodeBase):
    type: NodeType = Field(NodeType.START)
    id_of_true_condition: int


class MessageNode(NodeBase):
    type: NodeType = Field(NodeType.MESSAGE)
    message_text: str
    status: MessageNodeStatus
    id_of_true_condition: int


class ConditionNode(NodeBase):
    type: NodeType = Field(NodeType.CONDITION)
    condition: str

    id_of_true_condition: int
    id_of_false_condition: int


class EndNode(NodeBase):
    type: NodeType = Field(NodeType.END)
