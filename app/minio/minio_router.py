from io import BytesIO

from fastapi import APIRouter, Depends, File, UploadFile, status
from minio.error import S3Error, ServerError

from app.auth.auth_bearer import jwt_validator
from app.minio.minio_handler import MinioHandler

minio_router = APIRouter()

try:
    minio_instance = MinioHandler()
except S3Error as e:
    print(e)
except ServerError as e:
    print(e)


@minio_router.post("/upload", dependencies=[Depends(jwt_validator)], status_code=status.HTTP_201_CREATED)
async def upload_file_to_minio(file: UploadFile = File(...)):
    data = file.file.read()
    file_name = " ".join(file.filename.strip().split())
    try:
        detail = minio_instance.put_object(
            file_name=file_name,
            file_data=BytesIO(data),
            content_type=file.content_type
        )
        return detail
    except S3Error as e:
        print(e)


@minio_router.get("/download/{file_name}", dependencies=[Depends(jwt_validator)], status_code=status.HTTP_200_OK)
def download_file_from_minio(file_name: str):
    try:
        detail = minio_instance.get_object(file_name)
        return detail
    except S3Error as e:
        print(e)

@minio_router.get("/all", dependencies=[Depends(jwt_validator)], status_code=status.HTTP_200_OK)
def list_all_files():
    try:
        return [object for object in minio_instance.list_objects()]
    except S3Error as e:
        print(e)