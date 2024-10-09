from typing import List, Optional

from fastapi import APIRouter, Depends

from src.auth.dependency import get_uow, get_current_user, get_optional_current_user
from src.utils.unitofwork import IUnitOfWork
from .dependency import get_current_author
from .exceptions import unauthorized_exception
from .schemas import NewsCreate, NewsUpdate, NewsRead
from .service import NewsService

router = APIRouter(prefix="/api/v1/news", tags=["news"])


@router.post("", response_model=NewsRead)
async def create_news(news: NewsCreate,
                      uow: IUnitOfWork = Depends(get_uow),
                      current_author: UserRead = Depends(get_current_author)):
    news = await NewsService().create_news(uow, news, current_author.id)
    """Создание статьи могут только авторы"""
    return news


@router.get("/{news_id}", response_model=NewsRead)
async def read_news(news_id: int,
                    uow: IUnitOfWork = Depends(get_uow),
                    current_user: Optional[UserRead] = Depends(get_optional_current_user)):
    """Поиск"""
    news = await NewsService().get_news(uow, news_id)
    if not news.is_public and (not current_user or (current_user and current_user.role == "подписчик")):
        raise unauthorized_exception
    return news


@router.get("", response_model=List[NewsRead])
async def read_news_list(uow: IUnitOfWork = Depends(get_uow),
                         current_user: Optional[UserRead] = Depends(get_optional_current_user)):
    """выдает все статьи.
        Если авторизован то выдает и закрытые а если нет то только открытые"""
    if current_user:
        news_list = await NewsService().get_all_news(uow, is_public=None)
    else:
        news_list = await NewsService().get_all_news(uow, is_public=True)
    return news_list

@router.put("/{news_id}", response_model=NewsRead)
@router.patch("/{news_id}", response_model=NewsRead)
async def update_news(news_id: int, news: NewsUpdate,
                      uow: IUnitOfWork = Depends(get_uow),
                      current_author: UserRead = Depends(get_current_author)):
    await NewsService().update_news(uow, news_id, news, current_author.id)
    """Обновление статьи может только автор"""
    updated_news = await NewsService().get_news(uow, news_id)
    return updated_news


@router.delete("/{news_id}", status_code=204)
async def delete_news(news_id: int, uow: IUnitOfWork = Depends(get_uow),
                      current_author: UserRead = Depends(get_current_author)):
   await NewsService().delete_news(uow, news_id, current_author.id)
   """Удаляет"""
   return {"message": "deleted"}


@router.get("/author", response_model=List[NewsRead])
async def news_by_author(uow: IUnitOfWork = Depends(get_uow),
                         current_author: UserRead = Depends(get_current_author)):
    """Выдает все статьи который написал автор """
    news_list = await NewsService().get_news_by_author(uow, current_author.id)
    return news_list


