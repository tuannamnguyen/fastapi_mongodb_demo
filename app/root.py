from fastapi import FastAPI
from app.students.student_router import student_router

app = FastAPI()
app.include_router(student_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


