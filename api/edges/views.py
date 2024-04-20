from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from api.edges.crud import delete_edge, update_edge
from api.edges.schemas import EdgeBase
from core.database.database import get_async_session

router = APIRouter(tags=["Edges"])


@router.put("update/{edge_id}/")
async def update_view(
    edge_id: int,
    update_edge_in: EdgeBase,
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    await update_edge(
        session=session,
        edge_id=edge_id,
        edge_update=update_edge_in,
    )
    return Response(content={"status": "ok"}, status_code=200)


@router.delete("/{edge_id}/")
async def delete_edge_view(
    edge_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    await delete_edge(session=session, edge_id=edge_id)
    return Response(content={"status": "ok"}, status_code=200)
