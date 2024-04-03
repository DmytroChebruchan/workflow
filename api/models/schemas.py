from pydantic import BaseModel
from typing import List, Optional


class NodeBase(BaseModel):
    type: str


class NodeCreate(NodeBase):
    pass


class NodeUpdate(NodeBase):
    pass


class WorkflowBase(BaseModel):
    pass


class WorkflowCreate(WorkflowBase):
    pass


class WorkflowUpdate(WorkflowBase):
    pass
