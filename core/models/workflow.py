from sqlalchemy.orm import relationship

from .base import Base


class Workflow(Base):
    nodes = relationship("Node", back_populates="workflow")
