from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from core.models import Base, db_helper
from api import router


@asynccontextmanager
async def lifespan(app: FastAPI):

    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
