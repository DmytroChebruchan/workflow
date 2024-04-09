from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils import get_element_by_id
from api.workflows import crud
from core.models import Workflow, db_helper


async def workflow_validator(
    workflow_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    workflow = await get_element_by_id(
        session=session, element_id=workflow_id, element=Workflow
    )
    if workflow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow with ID {workflow_id} not found",
        )
    return workflow
