from pydantic import BaseModel


class NodeBase(BaseModel):
    type: str


class NodeCreate(NodeBase):
    workflow_id: int


class Node(NodeBase):
    id: int
    workflow_id: int

    class Config:
        orm_mode = True
