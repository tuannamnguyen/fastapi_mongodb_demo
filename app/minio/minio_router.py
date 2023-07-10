from io import BytesIO
from fastapi import File, UploadFile, APIRouter, Depends, status
from app.minio.minio_handler import MinioHandler
from app.auth.auth_bearer import jwt_validator
from minio.error import S3Error, ServerError


minio_router = APIRouter()

try:
    minio_instance = MinioHandler()
except S3Error as e:
    print("error occurred.", e)
except ServerError as e:
    print("error occurred.", e)


@minio_router.post("/upload", dependencies=[Depends(jwt_validator)], status_code=status.HTTP_201_CREATED)
async def upload_file_to_minio(file: UploadFile = File(...)):
    data = file.file.read()
    file_name = " ".join(file.filename.strip().split())

    return minio_instance.put_object(
        file_name=file_name,
        file_data=BytesIO(data),
        content_type=file.content_type
    )

@minio_router.get("/download/{file_name}", dependencies=[Depends(jwt_validator)], status_code=status.HTTP_200_OK)
def download_file_from_minio(file_name: str):
    return minio_instance.get_object(file_name)