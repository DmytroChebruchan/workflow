from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from starlette.testclient import TestClient

from main import app
from demo.samples_of_nodes import nodes_to_update, nodes_to_create

engine = create_async_engine("sqlite+aiosqlite:///db.sqlite3")
SessionLocal = async_sessionmaker(engine)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


def create_workflow():
    client = TestClient(app)
    # create workflow
    client.post("/workflows/create/", json={"title": "Test Workflow"})


def create_nodes(nodes: list):
    client = TestClient(app)
    for node in nodes:
        client.post("nodes/create/", json=node)
        print(f"{node.type} was created.")


def update_nodes(nodes):
    client = TestClient(app)
    for node in nodes:
        client.post(f"nodes/update/{node.id}", json=node)
        print(f"{node.type} was updated.")


def run_workflow():
    client = TestClient(app)
    result = client.get("/workflows/run/1")
    print(result.content)


def delete_workflow():
    client = TestClient(app)
    client.delete("/workflows/delete/1")
    print("workflow was deleted")


if __name__ == "__main__":
    # creating workflow
    create_workflow()

    # creating nodes related
    create_nodes(nodes_to_create)

    # updating edges
    update_nodes(nodes_to_update)

    # running workflow
    run_workflow()

    # clearing db
    delete_workflow()
