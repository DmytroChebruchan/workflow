from typing import Optional

from pydantic import BaseModel

from api.nodes.node_attr_values import NodeType


class NodeBase(BaseModel):
    type: NodeType
    workflow_id: int
    status: Optional[str]
    message_text: Optional[str]


class NodeCreate(NodeBase):
    pass


class NodeUpdate(NodeBase):
    id: int


class Node(NodeBase):
    id: int

    class Config:
        orm_mode = True
