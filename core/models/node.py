from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Node(Base):
    type = Column(String)
    workflow_id = Column(Integer, ForeignKey("workflows.id"))
    status = Column(String, nullable=True)
    message_text = Column(String, nullable=True)
    workflow = relationship("Workflow", back_populates="nodes")
    condition = Column(String, nullable=True)
