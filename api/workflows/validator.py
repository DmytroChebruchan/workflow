from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.workflows import crud
from core.models.db_helper import db_helper


async def workflow_validator(
    workflow_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    workflow = await crud.get_workflow_by_id(session, workflow_id)
    if workflow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow with ID {workflow_id} not found",
        )
    return workflow
