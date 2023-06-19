from fastapi import APIRouter, status, HTTPException, Depends, Response
from fastapi_redis_cache import cache
from fastapi.encoders import jsonable_encoder
from app.students.student_model import *
from app.auth.auth_bearer import jwt_validator
from decouple import config
import motor.motor_asyncio

DB_CONNECTION_STRING = config("db_connection_string")

# Connect to DB
client = motor.motor_asyncio.AsyncIOMotorClient(DB_CONNECTION_STRING)
db = client.demoapp

student_router = APIRouter()


@student_router.get("", dependencies=[Depends(jwt_validator)], status_code=status.HTTP_200_OK)
@cache(expire=30)
async def get_all_students(response: Response) -> list[dict]:
    response.headers["content-length"] = 2000
    return [bson_to_dict(student) async for student in db.students.find()]


@student_router.post("", dependencies=[Depends(jwt_validator)], status_code=status.HTTP_201_CREATED)
async def add_student(student: StudentModel) -> dict:
    student = jsonable_encoder(student)
    await db.students.insert_one(student)
    return bson_to_dict(student)


@student_router.get("/{student_id}", dependencies=[Depends(jwt_validator)], status_code=status.HTTP_200_OK)
async def get_student_by_id(student_id: int) -> dict:
    student = await db.students.find_one({"student_id": student_id})
    if student is not None:
        return bson_to_dict(student)
    raise HTTPException(
        status_code=404, detail=f"Student {student_id} not found")


@student_router.put("/{student_id}", dependencies=[Depends(jwt_validator)], status_code=status.HTTP_201_CREATED)
async def update_student_by_id(student_id: int, student_update_data: UpdateStudentModel) -> dict:
    student = await db.students.find_one({"student_id": student_id})
    student_update_data = jsonable_encoder(student_update_data)
    if student is not None:
        await db.students.update_one({"student_id": student_id}, {"$set": student_update_data})
        return bson_to_dict(student_update_data)
    raise HTTPException(
        status_code=404, detail=f"Student {student_id} not found")


@student_router.delete("/{student_id}", dependencies=[Depends(jwt_validator)], status_code=status.HTTP_200_OK)
async def delete_student_by_id(student_id: int) -> dict:
    student = await db.students.find_one({"student_id": student_id})
    if student is not None:
        await db.students.delete_one({"student_id": student_id})
        return bson_to_dict(student)
    raise HTTPException(
        status_code=404, detail=f"Student {student_id} not found")
