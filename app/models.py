from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId


class StudentModel(BaseModel):
    student_id: int
    fullname: str
    email: EmailStr
    gender: str = Field(..., regex='(?:m|M|male|Male|f|F|female|Female|FEMALE|MALE|Non-binary)$')
    major: str
    year: int = Field(..., gt=0, lt=4)
    gpa: float = Field(..., ge=0, le=4)

    class Config:
        schema_extra = {
            "example": {
                "student_id": "1",
                "fullname": "Andrea Croke",
                "email": "acrokeo4@123-reg.co.uk",
                "gender": "Male",
                "major": "Business Development",
                "year": 1,
                "gpa": 1.6,
            }
        }


class UpdateStudentModel(BaseModel):
    student_id: int | None
    fullname: str | None
    email: EmailStr | None
    gender: str | None = Field(regex='(?:m|M|male|Male|f|F|female|Female|FEMALE|MALE|Non-binary)$')
    major: str | None
    year: int | None = Field(gt=0, lt=4)
    gpa: float | None = Field(ge=0, le=4)

    class Config:
        schema_extra = {
            "example": {
                "student_id": "1",
                "fullname": "Andrea Croke",
                "email": "acrokeo4@123-reg.co.uk",
                "gender": "Male",
                "major": "Business Development",
                "year": 1,
                "gpa": 1.6,
            }
        }

