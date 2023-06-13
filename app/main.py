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
async def get_all_students() -> list[dict]:
    return [bson_to_dict(student) async for student in db.students.find()]


@app.post("/students", status_code=status.HTTP_201_CREATED)
async def add_student(student: StudentModel) -> dict:
    student = jsonable_encoder(student)
    await db.students.insert_one(student)
    return bson_to_dict(student)


@app.get("/students/{student_id}", status_code=status.HTTP_200_OK)
async def get_student_by_id(student_id: int) -> dict:
    student = await db.students.find_one({"student_id": student_id})
    if student is not None:
        return bson_to_dict(student)
    raise HTTPException(
        status_code=404, detail=f"Student {student_id} not found")


@app.put("/students/{student_id}", status_code=status.HTTP_201_CREATED)
async def update_student_by_id(student_id: int, student_update_data: UpdateStudentModel) -> dict:
    student = await db.students.find_one({"student_id": student_id})
    student_update_data = jsonable_encoder(student_update_data)
    if student is not None:
        await db.students.update_one({"student_id": student_id}, {"$set": student_update_data})
        return bson_to_dict(student_update_data)
    raise HTTPException(
        status_code=404, detail=f"Student {student_id} not found")


@app.delete("/students/{student_id}", status_code=status.HTTP_200_OK)
async def delete_student_by_id(student_id: int) -> dict:
    student = await db.students.find_one({"student_id": student_id})
    if student is not None:
        await db.students.delete_one({"student_id": student_id})
        return bson_to_dict(student)
    raise HTTPException(
        status_code=404, detail=f"Student {student_id} not found")