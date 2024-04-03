from fastapi import APIRouter
from api.models.schemas import NodeCreate, NodeUpdate

router = APIRouter()


@router.post("/add_node")
def add_node(node: NodeCreate):
    pass


@router.put("/update_node/{node_id}")
def update_node(node_id: int, node: NodeUpdate):
    pass


@router.delete("/delete_node/{node_id}")
def delete_node(node_id: int):
    pass
