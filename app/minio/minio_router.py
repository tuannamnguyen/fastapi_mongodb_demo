from io import BytesIO
from fastapi import File, UploadFile, APIRouter, Depends, status, HTTPException
from app.minio.minio_handler import MinioHandler
from app.minio.minio_model import *
from app.auth.auth_bearer import jwt_validator
from app.minio.exception import CustomException


minio_router = APIRouter()

try:
    minio_instance = MinioHandler()
except Exception as e:
    if e.__class__.__name__ == 'MaxRetryError':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot connect to server")


@minio_router.post("/upload", response_model=UploadFileResponse, dependencies=[Depends(jwt_validator)], status_code=status.HTTP_201_CREATED)
async def upload_file_to_minio(file: UploadFile = File(...)):
    data = file.file.read()
    file_name = " ".join(file.filename.strip().split())

    return minio_instance.put_object(
        file_name=file_name,
        file_data=BytesIO(data),
        content_type=file.content_type
    )

@minio_router.get("/download/{file_name}", status_code=status.HTTP_200_OK)
def download_file_from_minio(file_name: str):
    return minio_instance.get_object(file_name)

