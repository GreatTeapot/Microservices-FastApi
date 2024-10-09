from typing import List, Optional

from src.utils.unitofwork import IUnitOfWork
from .exceptions import news_not_found, unauthorized_exception
from .schemas import NewsCreate, NewsUpdate, NewsRead
from ..utils.repository import AbstractRepository


class NewsService:
    async def create_news(self, uow: IUnitOfWork, news: NewsCreate, author_id: int) :
        news_dict = news.model_dump()
        news_dict["author_id"] = author_id
        news_dict["is_public"] = news.is_public
        async with uow:
            news_id = await uow.news.add_one(news_dict)

            await uow.commit()
            return news_id

    async def get_news(self, uow: IUnitOfWork, news_id: int) :
        async with uow:
            news = await uow.news.find_one(id=news_id)
            if not news:
                raise news_not_found
            return news.to_read_model()

    async def get_all_news(self, uow: IUnitOfWork, is_public: Optional[bool] = None) -> List[NewsRead]:
        async with uow:
            news_list = await uow.news.find_all(is_public=is_public)
            return news_list


    async def get_news_by_author(self, uow: IUnitOfWork, author_id: int):
        async with uow:
            news_list = await uow.news.find_by_author(author_id)
            return news_list

    async def update_news(self, uow: IUnitOfWork, news_id: int, news: NewsUpdate, author_id:int) :
        news_dict = news.model_dump()
        async with uow:
            existing_news = await uow.news.find_one(id=news_id)
            if not existing_news:
                raise news_not_found
            if existing_news.author_id != author_id:
                raise unauthorized_exception
            await uow.news.edit_one(news_id, news_dict)
            await uow.commit()

    async def delete_news(self, uow: IUnitOfWork, news_id: int, author_id: int) :
        async with uow:
            news = await uow.news.find_one(id=news_id)
            if not news:
                raise news_not_found
            if news.author_id != author_id:
                raise unauthorized_exception
            await uow.news.delete_one(id=news_id)
            await uow.commit()
