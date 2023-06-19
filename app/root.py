from decouple import config
from fastapi import FastAPI, Request, Response
from fastapi_redis_cache import FastApiRedisCache, cache
from app.students.student_router import student_router
from app.users.user_router import user_router

app = FastAPI()
app.include_router(student_router, prefix="/students", tags=["Students"])
app.include_router(user_router, prefix="/users", tags=["Users"])

REDIS_URL = config("redis_url")

@app.on_event("startup")
def startup():
    redis_cache = FastApiRedisCache()
    redis_cache.init(
        host_url=REDIS_URL,
        prefix="myapi-cache",
        response_header="X-MyAPI-Cache",
        ignore_arg_types=[Request, Response]
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}
