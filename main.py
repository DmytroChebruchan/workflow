from fastapi import FastAPI
from api.endpoints import workflow, nodes, execution

app = FastAPI()

app.include_router(workflow.router)
app.include_router(nodes.router)
app.include_router(execution.router)
