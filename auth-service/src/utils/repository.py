from abc import ABC, abstractmethod

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, **filter_by):
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self, id: int, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def find_all(self, is_public: bool = None):
        stmt = select(self.model)
        if is_public is not None:
            stmt = stmt.where(self.model.is_public == is_public)
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res
    # async def find_all(self):
    #     stmt = select(self.model)
    #     res = await self.session.execute(stmt)
    #     return res.scalars().all()

    async def find_closed_news_by_id(self, news_id: int):
        stmt = select(self.model).where(
            self.model.is_public == False,
            self.model.id == news_id
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def find_by_author(self, author_id: int):
        stmt = select(self.model).where(self.model.author_id == author_id)
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res

    async def find_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def edit_one(self, id: int, data: dict):
        stmt = update(self.model).where(self.model.id == id).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete_one(self, id: int):
        stmt = delete(self.model).where(self.model.id == id).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()
