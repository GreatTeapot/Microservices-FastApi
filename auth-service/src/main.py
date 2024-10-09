from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from src.auth.router import router as auth_router
from src.auth.service import UserService
from src.utils.unitofwork import UnitOfWork

app = FastAPI(
    title="Documentation for Auth service",

)

app.mount("/static", StaticFiles(directory="src/static"), name="static")


origins = [
    "http://localhost:3000",
]

app.include_router(auth_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)



@app.on_event("startup")
async def startup_event():
    uow = UnitOfWork()
    await UserService().create_default_superuser(uow)

#
# @app.on_event("startup")
# async def startup_event():
#     redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

