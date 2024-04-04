from typing import Optional

from pydantic import BaseModel
from enum import Enum


class MessageNodeStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    OPENED = "opened"


class NodeType(str, Enum):
    START = "Start Node"
    MESSAGE = "Message Node"
    CONDITION = "Condition Node"
    END = "End Node"


class NodeBase(BaseModel):
    type: NodeType


class NodeCreate(NodeBase):
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
