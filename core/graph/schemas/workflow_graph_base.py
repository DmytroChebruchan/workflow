from typing import List

import networkx as nx

from core.models import Edge, Node


class WorkflowGraphBase:
    graph: nx.DiGraph
    nodes: List[Node]
    edges: List[Edge]
    start_node: Node
    end_node: Node
