from fastapi import Depends

from src.auth.dependency import get_current_user
from src.auth.exceptions import credentials_exception
from src.auth.schemas import UserRead


async def get_current_author(current_user: UserRead = Depends(get_current_user)):
    if current_user.role != "автор":
        raise credentials_exception
    return current_user