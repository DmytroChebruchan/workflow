from typing import Optional

from pydantic import BaseModel, ConfigDict

from api.nodes.node_attr_values import MessageNodeStatus, NodeType


class NodeBase(BaseModel):
    type: NodeType
    workflow_id: int
    status: Optional[str] = None
    message_text: Optional[str] = None
    condition: Optional[str] = None

    model_config = ConfigDict()


class NodeCreate(NodeBase):
    id_of_true_condition: Optional[int] = None
    id_of_false_condition: Optional[int] = None


class NodeUpdate(NodeBase):
    id: int


class Node(NodeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class MessageNode(NodeBase):
    status: MessageNodeStatus
    message_text: str


class ConditionNode(NodeBase):
    condition: str
