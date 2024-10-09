from datetime import datetime

from sqlalchemy import Integer, String, Text, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base
from src.news.schemas import NewsRead

class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)


    def to_read_model(self) -> NewsRead:

        return NewsRead(
            id=self.id,
            title=self.title,
            content=self.content,
            author_id=self.author_id,
            is_public=self.is_public,
            created_at=self.created_at,
            updated_at=self.updated_at,

        )
