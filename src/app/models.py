from pydantic import BaseModel, Field, EmailStr


class StudentModel(BaseModel):
    student_id: str
    fullname: str
    email_addr: EmailStr
    major: str
    year: int = Field(..., gt=0,lt=4)
    gpa: float = Field(..., ge=0,le=4)

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
    email_addr: EmailStr | None
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
