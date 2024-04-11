from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.edge.crud import create_edge
from api.nodes.crud import create_node
from api.workflows.schemas import WorkflowCreate, WorkflowUpdate
from core.models.node import Node
from core.models.workflow import Workflow


async def get_workflows(session: AsyncSession) -> list[Workflow]:
    stmt = select(Workflow).order_by(Workflow.id)
    result: Result = await session.execute(stmt)
    workflows = result.scalars().all()
    return list(workflows)


async def get_workflow_by_id(
    session: AsyncSession, workflow_id: int
) -> Workflow | None:
    return await session.get(Workflow, workflow_id)


async def create_workflow(session: AsyncSession, workflow_in: WorkflowCreate):
    # Create and add the workflow to the session
    workflow = Workflow(**workflow_in.model_dump())
    session.add(workflow)
    await session.commit()
    await session.refresh(workflow)
    return workflow


async def update_workflow(
    session: AsyncSession,
    workflow_update: WorkflowUpdate,
    workflow,
) -> Workflow | None:

    for field, value in workflow_update.dict(exclude_unset=True).items():
        setattr(workflow, field, value)

    await session.commit()
    await session.refresh(workflow)
    return workflow


async def delete_workflow_by_id(
    session: AsyncSession, workflow: Workflow
) -> None:
    await session.delete(workflow)
    await session.commit()
    await session.refresh(workflow)


async def create_workflow_with_nodes(
    session: AsyncSession, workflow_in: WorkflowCreate
):
    # Create and add the workflow to the session
    workflow = await create_workflow(session=session, workflow_in=workflow_in)

    # Create start and end nodes associated with the workflow
    start_node = Node(type="Start Node", workflow_id=workflow.id)
    created_start_node = create_node(start_node)
    end_node = Node(type="End Node", workflow_id=workflow.id)
    created_end_node = create_node(end_node)

    # Create an edge connecting the start and end nodes
    await create_edge(
        from_node_id=created_start_node.id, to_node_id=created_end_node.id
    )
    return workflow
