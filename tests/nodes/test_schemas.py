import pytest
from pydantic import ValidationError

from api.nodes.schemas import NodeCreate, NodeUpdate
from tests.nodes.fixture_nodes_dicts import (
    dummy_condition_node,
    dummy_message_node,
    dummy_node,
    dummy_start_node,
)


def test_node_create():
    node_data = dummy_node
    node = NodeCreate(**node_data)
    assert node.type == dummy_node["type"]
    assert node.workflow_id == dummy_node["workflow_id"]


def test_node_update():
    node_data = dummy_start_node
    node = NodeUpdate(**node_data)
    assert node.id == dummy_start_node["id"]
    assert node.workflow_id == dummy_start_node["workflow_id"]
    assert node.type == dummy_start_node["type"]


def test_node_invalid_data():
    with pytest.raises(ValidationError):
        NodeCreate()
