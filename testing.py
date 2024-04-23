from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Define a base class for our ORM models
Base = declarative_base()


# Define the Node class
class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Define the relationship with edges
    incoming_edges = relationship(
        "Edge",
        back_populates="destination",
        foreign_keys="[Edge.destination_id]",
    )
    outgoing_edges = relationship(
        "Edge", back_populates="source", foreign_keys="[Edge.source_id]"
    )


# Define the Edge class
class Edge(Base):
    __tablename__ = "edges"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    source_id = Column(Integer, ForeignKey("nodes.id"))
    destination_id = Column(Integer, ForeignKey("nodes.id"))

    # Define the relationship with nodes
    source = relationship("Node", back_populates="outgoing_edges")
    destination = relationship("Node", back_populates="incoming_edges")
