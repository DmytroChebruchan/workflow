from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.edges.crud import delete_edge
from core.database.database import get_async_session

router = APIRouter(tags=["Edges"])


@router.delete("/{edge_id}/")
async def delete_edge_view(
    edge_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    await delete_edge(session=session, edge_id=edge_id)
    return Response(content={"status": "ok"}, status_code=200)
