from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import Base


class Workflow(Base):
    title = Column(String, nullable=True)
    nodes = relationship("Node", back_populates="workflow")
