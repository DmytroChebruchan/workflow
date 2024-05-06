import unittest
from unittest.mock import MagicMock, patch

from core.graph.script import creating_graph_script


class TestCreatingGraphScript(unittest.TestCase):
    @patch("api.general.utils.get_edges_of_nodes")
    @patch("api.general.utils.WorkflowGraph")
    async def test_creating_graph_script(
        self, mock_workflow_graph, mock_get_edges_of_nodes
    ):
        # Mocking the session and workflow objects
        session = MagicMock()
        workflow = MagicMock()
        workflow.nodes = ["node1", "node2", "node3"]  # Sample nodes

        # Mocking the return value of get_edges_of_nodes
        mock_get_edges_of_nodes.return_value = [
            ("node1", "node2"),
            ("node2", "node3"),
        ]  # Sample edges

        # Calling the function
        result = await creating_graph_script(session, workflow)

        # Asserting that get_edges_of_nodes was called
        # with the correct arguments
        mock_get_edges_of_nodes.assert_called_once_with(
            ["node1", "node2", "node3"]
        )

        # Asserting that WorkflowGraph was initialized with the
        # correct arguments
        mock_workflow_graph.assert_called_once_with(
            nodes=["node1", "node2", "node3"],
            edges=[("node1", "node2"), ("node2", "node3")],
            session=session,
        )

        # Asserting the return value
        self.assertEqual(result, mock_workflow_graph.return_value)


if __name__ == "__main__":
    unittest.main()
