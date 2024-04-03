import networkx as nx
from core.models import Workflow, Node
from typing import List


class WorkflowEngine:
    def __init__(self):
        pass

    def build_graph(self, workflow: Workflow) -> nx.DiGraph:
        pass

    def execute_workflow(self, workflow: Workflow) -> List[Node]:
        pass

    def find_path(
        self, graph: nx.DiGraph, start_node: Node, end_node: Node
    ) -> List[Node]:
        pass
