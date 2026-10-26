from datetime import datetime

from pydantic import ConfigDict, BaseModel


class DocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)


    id: int
    filename: str
    status: str
    created_at: datetime