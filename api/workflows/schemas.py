from pydantic import BaseModel, ConfigDict


class WorkflowBase(BaseModel):
    pass


class WorkflowCreate(WorkflowBase):
    pass


class Workflow(WorkflowBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
