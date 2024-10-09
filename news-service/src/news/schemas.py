from datetime import datetime
from pydantic import BaseModel


class NewsBase(BaseModel):
    title: str
    content: str
    is_public: bool


class NewsCreate(NewsBase):
    pass


class NewsUpdate(NewsBase):
    pass


class NewsRead(NewsBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
