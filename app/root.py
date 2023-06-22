from fastapi import FastAPI
from fastapi_redis_cache import FastApiRedisCache
from app.students.student_router import student_router
from app.users.user_router import user_router
from decouple import config

REDIS_URL = config("redis_url")

app = FastAPI()
app.include_router(student_router, prefix="/students", tags=["Students"])
app.include_router(user_router, prefix="/users", tags=["Users"])


@app.on_event("startup")
def startup():
    redis_cache = FastApiRedisCache()
    redis_cache.init(
        host_url=REDIS_URL,
        prefix="myapi-cache",
        response_header="X-MyAPI-Cache",
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}
