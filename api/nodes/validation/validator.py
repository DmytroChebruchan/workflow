from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.general.utils_ElementRepo import ElementRepo
from api.nodes.node_attr_values import NodeType
from api.nodes.node_handling import get_nodes_by_type
from api.nodes.schemas.schemas_by_nodes_creating_stage import NodeCreate
from api.workflows.crud_WorkflowRepo import WorkflowRepo
from core.models import Node


async def check_node_type_existence_in_workflow(
    node_in: NodeCreate, session: AsyncSession
) -> None:

    # collecting values fot check
    workflow_id = node_in.workflow_id
    workflow_object = WorkflowRepo(session=session, workflow_id=workflow_id)
    await workflow_object.get_workflow_by_id()
    node_type = node_in.type

    # checker
    await ensure_unique_node_type(
        node_type=node_type,
        workflow_id=workflow_id,
        session=session,
    )


async def ensure_unique_node_type(
    node_type: str, workflow_id: int, session: AsyncSession
):
    if node_type != NodeType.START and node_type != NodeType.END:
        return

    nodes_of_type = await get_nodes_by_type(
        session, node_type=node_type, workflow_id=workflow_id
    )

    if nodes_of_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Workflow with ID {workflow_id} has a {node_type}",
        )


async def check_edge_to_start_node(
    session: AsyncSession, nodes_dest_dict: dict
):
    if nodes_dest_dict is None:
        return
    nodes_ids = [nodes_dest_dict[key] for key in nodes_dest_dict]
    for node_id in nodes_ids:
        node_object = ElementRepo(session=session, model=Node)
        node = await node_object.get_element_by_id(element_id=node_id)
        if node.type == NodeType.START:
            raise Exception(
                f"Node {node_id} is Start Node and no edge can point to Start"
                f"Node."
            )
