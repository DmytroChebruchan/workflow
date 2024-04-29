from pydantic import BaseModel, ConfigDict


class WorkflowBase(BaseModel):
    title: str
    model_config = ConfigDict()


class WorkflowCreate(WorkflowBase):
    pass


class WorkflowUpdate(WorkflowBase):
    pass


class WorkflowFromDB(WorkflowBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
