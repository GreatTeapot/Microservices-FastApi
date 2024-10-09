from src.config import SUPER_USER_EMAIL, SUPER_USER_PASSWORD
from src.utils.unitofwork import IUnitOfWork
from fastapi import Response
from src.utils.utils import get_password_hash, verify_password
from .exceptions import (
    validate_user_existence,
    validate_user_authentication,
    credentials_exception,
    user_already_exists_exception,
)
from .jwt import create_access_token, decode_token, create_refresh_token
from .schemas import UserCreate, UserUpdate, PasswordChange, SuperUser


class UserService:
    async def _create_user(self, uow: IUnitOfWork, response: Response = None, user_data: dict = None, role: str = "subscriber", is_superuser: bool = False):
        async with uow:
            password = get_password_hash(user_data.pop("password"))
            user_data["password"] = password
            user_data["role"] = role
            user_data["is_superuser"] = is_superuser

            existing_user = await uow.users.find_one(email=user_data["email"])
            if existing_user:
                raise user_already_exists_exception

            user = await uow.users.add_one(user_data)
            await uow.commit()

            if response:
                response.set_cookie(key="access_token", value=f"Bearer: {create_access_token({'sub': str(user)})}")
                response.set_cookie(key="refresh_token", value=f"Bearer: {create_refresh_token({'sub': str(user)})}", httponly=True)
            return {"message": "User created successfully",
                    "user_id": user.id,
                    "access_token": create_access_token({"sub": str(user)})}

    async def create_user(self, uow: IUnitOfWork, response: Response, user: UserCreate, role: str = "subscriber"):
        user_data = user.model_dump()
        return await self._create_user(uow, response, user_data, role=role)

    async def create_superuser(self, uow: IUnitOfWork, user: SuperUser):
        user_data = user.model_dump()
        return await self._create_user(uow, user_data=user_data, role="superuser", is_superuser=True)

    async def update_superuser(self, uow: IUnitOfWork, user: SuperUser):
        user_data = user.model_dump()
        async with uow:
            password = get_password_hash(user_data.pop("password"))
            user_data["password"] = password
            user_data["is_superuser"] = True

            existing_user = await uow.users.find_one(email=user_data["email"])
            if existing_user:
                await uow.users.edit_one(existing_user.id, user_data)
                user_id = existing_user.id
            else:
                user_id = await uow.users.add_one(user_data)

            await uow.commit()

    async def create_default_superuser(self, uow: IUnitOfWork):
        superuser_data = SuperUser(
            email=SUPER_USER_EMAIL,
            password=SUPER_USER_PASSWORD,
            role = "superuser",
            is_superuser=True
        )
        await self.update_superuser(uow, superuser_data)


    async def authenticate_user(self, response:Response, uow: IUnitOfWork, email: str, password: str):
        async with uow:
            user = await uow.users.find_one(email=email)
            validate_user_authentication(user)

            user.is_verified = True
            await uow.users.edit_one(user.id, {"is_verified": True})
            if response:
                response.set_cookie(key="access_token", value=f"Bearer: {create_access_token({'sub': str(user)})}")
                response.set_cookie(key="refresh_token", value=f"Bearer: {create_refresh_token({'sub': str(user)})}",
                                    httponly=True)

            await uow.commit()
            return {"message": "logged in successfully",
                    "user_id": user.id,
                    "access_token": create_access_token({"sub": str(user)})}

    async def get_user(self, uow: IUnitOfWork, user_id: int):
        async with uow:
            user = await uow.users.find_one(id=user_id)
            validate_user_existence(user)
            return user.to_read_model()

    async def get_all_users(self, uow: IUnitOfWork):
        async with uow:
            users = await uow.users.find_all()
            return users

    async def update_user(self, uow: IUnitOfWork, user_id: int, user: UserUpdate):
        user_data = user.model_dump()
        async with uow:
            existing_user = await uow.users.find_one(id=user_id)
            validate_user_existence(existing_user)
            await uow.users.edit_one(user_id, user_data)
            await uow.commit()
            return user.to_read_model()

    async def delete_user(self, uow: IUnitOfWork, user_id: int):
        async with uow:
            user = await uow.users.find_one(id=user_id)
            validate_user_existence(user)
            await uow.users.delete_one(id=user_id)
            await uow.commit()

    async def change_password(self, uow: IUnitOfWork, user_id: int, password_data: PasswordChange):
        async with uow:
            user = await uow.users.find_one(id=user_id)
            validate_user_existence(user)
            if not verify_password(password_data.old_password, user.password):
                validate_user_authentication(None)
            user.password = get_password_hash(password_data.new_password)
            await uow.users.edit_one(user_id, {"password": user})
            await uow.commit()

    async def refresh_access_token(self, refresh_token: str):
        payload = decode_token(refresh_token)
        if not payload:
            raise credentials_exception
        user_id = payload.get("sub")
        return create_access_token({"sub": user_id})

    async def logout(self, refresh_token: str):
        payload = decode_token(refresh_token)
        if not payload:
            raise credentials_exception


