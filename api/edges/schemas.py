from typing import Optional

from pydantic import BaseModel, ConfigDict


class EdgeBase(BaseModel):
    source_node_id: int
    destination_node_id: int
    condition: Optional[bool] = None
    model_config = ConfigDict()
