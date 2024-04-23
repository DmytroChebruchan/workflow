from pydantic.fields import Field

from api.nodes.node_attr_values import MessageNodeStatus, NodeType
from api.nodes.schemas.schemas import NodeBase


class StartNode(NodeBase):
    type: NodeType = Field(NodeType.START)


class MessageNode(NodeBase):
    type: NodeType = Field(NodeType.MESSAGE)
    message_text: str
    status: MessageNodeStatus


class ConditionNode(NodeBase):
    type: NodeType = Field(NodeType.CONDITION)
    condition: str


class EndNode(NodeBase):
    type: NodeType = Field(NodeType.END)
