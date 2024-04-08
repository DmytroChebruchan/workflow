from fastapi import APIRouter

router = APIRouter(tags=["General"])


@router.post("/health_check/")
async def health_check():
    return {"message": "Healthy"}
