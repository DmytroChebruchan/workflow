from typing import Optional, List, Union

from pydantic import BaseModel, ConfigDict

from api.nodes.node_attr_values import MessageNodeStatus, NodeType


class NodeBase(BaseModel):
    type: NodeType
    workflow_id: int
    message_text: Optional[str] = None
    status: Optional[str] = None
    condition: Optional[str] = None
    model_config = ConfigDict()


class NodeCreate(NodeBase):
    from_node_id: Optional[int] | None = None
    to_node_id: Optional[int] | None = None
    nodes_to_list: Optional[List[dict]] = None


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
