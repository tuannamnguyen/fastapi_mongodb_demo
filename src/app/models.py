from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId


class StudentModel(BaseModel):
    id: int
    fullname: str
    email: EmailStr
    major: str
    year: int = Field(..., gt=0, lt=4)
    gpa: float = Field(..., ge=0, le=4)

    class Config:
        schema_extra = {
            "example": {
                "student_id": 869,
                "fullname": "Andrea Croke",
                "email": "acrokeo4@123-reg.co.uk",
                "major": "Business Development",
                "year": 1,
                "gpa": 1.6,
            }
        }


class UpdateStudentModel(BaseModel):
    fullname: str | None
    email: EmailStr | None
    major: str | None
    year: int | None
    gpa: float | None

    class Config:
        schema_extra = {
            "example": {
                "student_id": 869,
                "fullname": "Andrea Croke",
                "email": "acrokeo4@123-reg.co.uk",
                "major": "Business Development",
                "year": 1,
                "gpa": 1.6,
            }
        }

