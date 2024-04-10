from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from core.models.base import Base

engine = create_async_engine(
    "sqlite+aiosqlite:///db.sqlite3", connect_args={"check_same_thread": False}
)
SessionLocal = async_sessionmaker(engine)


async def get_db() -> AsyncSession:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
