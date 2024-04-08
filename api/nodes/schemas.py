from typing import Optional

from pydantic import BaseModel, ConfigDict

from api.nodes.node_attr_values import NodeType


class NodeBase(BaseModel):
    type: NodeType
    workflow_id: int
    status: Optional[str] = None
    message_text: Optional[str] = None

    model_config = ConfigDict(env_prefix="NODE_")


class NodeCreate(NodeBase):
    pass


class NodeUpdate(NodeBase):
    id: int


class Node(NodeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
