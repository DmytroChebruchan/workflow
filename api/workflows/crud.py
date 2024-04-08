from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.edge.schemas import EdgeBase
from api.workflows.schemas import WorkflowCreate, WorkflowUpdate
from core.models import Edge, Node, Workflow


async def get_workflows(session: AsyncSession) -> list[Workflow]:
    stmt = select(Workflow).order_by(Workflow.id)
    result: Result = await session.execute(stmt)
    workflows = result.scalars().all()
    return list(workflows)


async def get_workflow_by_id(
    session: AsyncSession, workflow_id: int
) -> Workflow | None:
    return await session.get(Workflow, workflow_id)


async def create_workflow(
    session: AsyncSession, workflow_in: WorkflowCreate
) -> Workflow:
    # Create and add the workflow to the session
    workflow = Workflow(**workflow_in.model_dump())
    session.add(workflow)
    await session.commit()
    await session.refresh(workflow)

    # Create start and end nodes associated with the workflow
    start_node = Node(type="Start Node", workflow_id=workflow.id)
    end_node = Node(type="End Node", workflow_id=workflow.id)
    session.add_all([start_node, end_node])
    await session.commit()

    # Create an edge connecting the start and end nodes
    edge = Edge(
        source_node_id=start_node.id,
        destination_node_id=end_node.id,
    )
    session.add(edge)
    await session.commit()

    # Refresh objects to get their updated attributes
    await session.refresh(start_node)
    await session.refresh(end_node)
    await session.refresh(edge)

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


async def delete_workflow_by_id(session: AsyncSession, workflow: Workflow) -> None:
    await session.delete(workflow)
    await session.commit()
    await session.refresh(workflow)
