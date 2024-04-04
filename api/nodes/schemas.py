from pydantic import BaseModel
from enum import Enum


class NodeType(str, Enum):
    START = "Start Node"
    MESSAGE = "Message Node"
    CONDITION = "Condition Node"
    END = "End Node"


class NodeBase(BaseModel):
    type: NodeType


class NodeCreate(NodeBase):
    workflow_id: int


class Node(NodeBase):
    id: int
    workflow_id: int

    class Config:
        orm_mode = True
