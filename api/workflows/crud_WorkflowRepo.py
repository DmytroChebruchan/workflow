from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils_element_class import ElementRepo
from api.workflows.schemas import WorkflowCreate, WorkflowUpdate
from core.models.workflow import Workflow


class WorkflowRepo(ElementRepo):
    model = Workflow
    object_of_class: Workflow

    def __init__(self, session: AsyncSession, workflow_id: int = None):
        super().__init__(session=session, model=self.model)
        self.workflow_id = workflow_id

    async def create_workflow(self, workflow_in: WorkflowCreate) -> Workflow:
        workflow = self.model(**workflow_in.model_dump())
        self.object_of_class = workflow
        await self.save_element_into_db()
        return workflow

    async def get_workflow_by_id(self) -> Workflow:
        self.object_of_class = await self.get_element_by_id(
            element_id=self.workflow_id,
        )
        return self.object_of_class

    async def update_workflow(
        self, workflow_update: WorkflowUpdate, workflow: Workflow
    ) -> Workflow:
        for field, value in workflow_update.model_dump(
            exclude_unset=True
        ).items():
            setattr(self.object_of_class, field, value)

        self.object_of_class = workflow
        await self.commit_and_refresh_element()
        return self.object_of_class

    async def delete_workflow_by_id(self) -> None:
        await self.delete_element_from_db()
