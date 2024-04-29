from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from api.nodes.node_attr_values import NodeType


class NodeBase(BaseModel):
    type: NodeType
    workflow_id: int
    status: Optional[str] = None
    condition: Optional[str] = None
    model_config = ConfigDict()


class NodeCreate(NodeBase):
    from_node_id: Optional[int] | None = None
    nodes_dest_dict: Optional[dict] | None = None
    edge_condition_type: Optional[bool] = True
    message_text: Optional[str] = None


class NodeUpdate(NodeBase):
    id: int
    message_text: Optional[str] = None
    from_node_id: Optional[int] | None = None
    nodes_dest_dict: List[dict] | list = []


class NodeFromDB(NodeBase):
    id: int
    message_text: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
