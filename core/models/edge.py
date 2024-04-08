from sqlalchemy import Column, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship

from core.models.base import Base


class Edge(Base):
    id = Column(Integer, primary_key=True)
    source_node_id = Column(Integer, ForeignKey("nodes.id"))
    destination_node_id = Column(Integer, ForeignKey("nodes.id"))
    condition_type = Column(Boolean, default=False, nullable=True)
    source_node = relationship(
        "Node",
        back_populates="outgoing_edges",
    )
    destination_node = relationship(
        "Node",
        back_populates="incoming_edges",
    )
