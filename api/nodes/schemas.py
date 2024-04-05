from typing import Optional

from pydantic import BaseModel

from api.nodes.node_attr_values import NodeType


class NodeBase(BaseModel):
    type: NodeType


class NodeCreate(NodeBase):
    workflow_id: int
    status: Optional[str]
    message_text: Optional[str]


class NodeUpdate(NodeBase):
    workflow_id: int
    status: Optional[str]
    message_text: Optional[str]


class Node(NodeBase):
    id: int
    workflow_id: int
    status: Optional[str]
    message_text: Optional[str]

    class Config:
        orm_mode = True
