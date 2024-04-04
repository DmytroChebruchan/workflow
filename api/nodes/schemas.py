from pydantic import BaseModel, ConfigDict


class NodeBase(BaseModel):
    pass


class NodeCreate(NodeBase):
    pass


class Node(NodeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
