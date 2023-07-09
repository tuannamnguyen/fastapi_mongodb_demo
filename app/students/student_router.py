from fastapi import APIRouter, status, HTTPException, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi_redis_cache import cache_one_minute
from app.students.student_schema import StudentSchema, UpdateStudentSchema
from app.auth.auth_bearer import jwt_validator
from app.students.student_model import Student, StudentUpdate

student_router = APIRouter()


@student_router.get("", dependencies=[Depends(jwt_validator)], status_code=status.HTTP_200_OK)
@cache_one_minute()
async def get_all_students(response: Response) -> list[dict]:
    return [student.dump() async for student in Student.find()]


@student_router.post("", dependencies=[Depends(jwt_validator)], status_code=status.HTTP_201_CREATED)
async def add_student(student: StudentSchema) -> dict:
    student_json = jsonable_encoder(student)
    await Student.ensure_indexes()
    await Student(**student_json).commit()
    return Student(**student_json).dump()


@student_router.get("/{student_id}", dependencies=[Depends(jwt_validator)], status_code=status.HTTP_200_OK)
async def get_student_by_id(student_id: int) -> dict:
    student = await Student.find_one({"student_id": student_id})
    if student:
        return student.dump()
    raise HTTPException(
        status_code=404, detail=f"Student {student_id} not found")


@student_router.put("/{student_id}", dependencies=[Depends(jwt_validator)], status_code=status.HTTP_201_CREATED)
async def update_student_by_id(student_id: int, student_update_data: UpdateStudentSchema) -> dict:
    student = await Student.find_one({"student_id": student_id})
    student_update_data = jsonable_encoder(student_update_data)
    student_update_data = {k: v for k,
                           v in student_update_data.items() if v is not None}
    if student:
        await StudentUpdate.collection.update_one({"student_id": student_id}, {"$set": student_update_data})
        return Student(**student_update_data).dump()
    raise HTTPException(
        status_code=404, detail=f"Student {student_id} not found")


@student_router.delete("/{student_id}", dependencies=[Depends(jwt_validator)], status_code=status.HTTP_200_OK)
async def delete_student_by_id(student_id: int) -> dict:
    student = await Student.find_one({"student_id": student_id})
    if student:
        await Student.collection.delete_one({"student_id": student_id})
        return student.dump()
    raise HTTPException(
        status_code=404, detail=f"Student {student_id} not found")
