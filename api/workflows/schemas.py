from pydantic import BaseModel, ConfigDict


class WorkflowBase(BaseModel):
    title: str


class WorkflowCreate(WorkflowBase):
    pass


class WorkflowUpdate(WorkflowBase):
    id: int


class Workflow(WorkflowBase):
    id: int
    title: str
