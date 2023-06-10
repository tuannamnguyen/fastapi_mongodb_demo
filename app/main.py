from fastapi import FastAPI, status, HTTPException
from fastapi.encoders import jsonable_encoder
from models import *
import motor.motor_asyncio

# Connect to DB
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
db = client.demoapp


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/students", status_code=status.HTTP_200_OK)
async def get_all_students():
    students = await db.students.find().to_list(1000)
    return students


@app.post("/students", status_code=status.HTTP_201_CREATED)
async def add_student(student: StudentModel):
    student = jsonable_encoder(student)
    result = await db.students.insert_one(student)
    return student


@app.get("/students/{id}", status_code=status.HTTP_200_OK)
async def get_student_by_id(id: int):
    student = await db.students.find_one({"_id": id})
    if student is not None: 
        return student
    raise HTTPException(status_code=404, detail=f"Student {id} not found")

