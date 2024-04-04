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
