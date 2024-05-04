from pydantic import field_validator
from pydantic.fields import Field

from api.nodes.node_attr_values import MessageNodeStatus, NodeType
from api.nodes.schemas.schemas_by_nodes_creating_stage import NodeBase


class StartNode(NodeBase):
    type: NodeType = Field(NodeType.START)


class MessageNode(NodeBase):
    type: NodeType = Field(NodeType.MESSAGE)
    message_text: str
    status: MessageNodeStatus
    from_node_id: int
    nodes_dest_dict: dict
    edge_condition_type: bool

    @field_validator("nodes_dest_dict")
    def validate_nodes_dest_dict(cls, v):
        if len(v) != 1:
            raise ValueError(
                'nodes_dest_dict must contain exactly 1 key: "true"'
            )
        if next(iter(v)) not in (True, False):
            raise ValueError(
                'nodes_dest_dict must contain exactly "true"' " conditions."
            )


class ConditionNode(NodeBase):
    type: NodeType = Field(NodeType.CONDITION)
    from_node_id: int
    nodes_dest_dict: dict
    edge_condition_type: bool
    condition: MessageNodeStatus

    @field_validator("nodes_dest_dict")
    def validate_nodes_dest_dict(cls, v):
        if len(v) not in [1, 2]:
            raise ValueError(
                "nodes_dest_dict must contain exactly 1 or 2 keys:"
                '"true" and "false"'
            )
        if set(v) in (True, False):
            raise ValueError(
                'nodes_dest_dict must contain exactly "true" or/and "false"'
            )
        if v[True] == v[False]:
            raise ValueError(
                "Both conditions can not target to the same node."
            )
        return v


class EndNode(NodeBase):
    type: NodeType = Field(NodeType.END)
    from_node_id: int
    edge_condition_type: bool
