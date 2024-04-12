from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.models.base import Base
# fmt: off
from core.models.edge import Edge
# fmt: on


class Node(Base):
    type = Column(String)
    status = Column(String, nullable=True)
    message_text = Column(String, nullable=True)
    condition = Column(String, nullable=True)

    workflow_id = Column(Integer, ForeignKey("workflows.id"))
    id_of_true_condition = Column(Integer, nullable=True)
    id_of_false_condition = Column(Integer, nullable=True)

    workflow = relationship("Workflow", back_populates="nodes")
    outgoing_edges = relationship(
        "Edge",
        foreign_keys="[Edge.source_node_id]",
        back_populates="source_node",
    )
    incoming_edges = relationship(
        "Edge",
        foreign_keys="[Edge.destination_node_id]",
        back_populates="destination_node",
    )
