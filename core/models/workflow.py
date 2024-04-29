from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from core.models.base import Base


class Workflow(Base):
    title = Column(String, nullable=True)
    nodes = relationship(
        "Node",
        back_populates="workflow",
        lazy="selectin",
    )

    def __str__(self):
        return f"Workflow {self.title}"
