from typing import List


class Node:
    def __init__(self, node_id: int):
        self.node_id = node_id
        self.type = None
        self.edges = []

    def add_edge(self, edge):
        pass

    def remove_edge(self, edge):
        pass


class Workflow:
    def __init__(self, workflow_id: int):
        self.workflow_id = workflow_id
        self.nodes: List[Node] = []

    def add_node(self, node: Node):
        pass

    def remove_node(self, node: Node):
        pass
