from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from core.models.base import Base


class Edge(Base):
    source_node_id = Column(Integer, ForeignKey("nodes.id"))
    destination_node_id = Column(Integer, ForeignKey("nodes.id"))
    condition_type = Column(Boolean, default=False, nullable=True)

    # relationship
    source_node = relationship(
        "Node",
        foreign_keys="[Edge.source_node_id]",
        back_populates="outgoing_edges",
        lazy="selectin",
    )
    destination_node = relationship(
        "Node",
        foreign_keys="[Edge.destination_node_id]",
        back_populates="incoming_edges",
        lazy="selectin",
    )

    def __str__(self):
        return (
            f"Edge between nodes "
            f"{self.source_node_id} -> {self.destination_node_id}"
        )
