import uuid
from sqlmodel import SQLModel, Field

class File(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=lambda: uuid.uuid4(), primary_key=True)
    nama: str = Field(default=None)
    path: str = Field(default=None)
    size: float = Field(default=None)
    type: str = Field(default=None)