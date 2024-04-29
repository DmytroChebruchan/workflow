from fastapi import HTTPException
from starlette import status


async def element_validator(element_id: int, item) -> None:
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{item} with ID {element_id} not found",
        )
