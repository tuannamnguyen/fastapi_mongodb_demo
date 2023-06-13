from fastapi import FastAPI
from app.students.student_router import student_router
from app.users.user_router import user_router

app = FastAPI()
app.include_router(student_router, prefix="/students", tags=["Students"])
app.include_router(user_router, prefix="/users", tags=["Users"])


@app.get("/")
async def root():
    return {"message": "Hello World"}
