from io import BytesIO
from fastapi import File, UploadFile, APIRouter, Depends, status
from app.minio.minio_handler import MinioHandler
from app.minio.minio_model import *
from app.auth.auth_bearer import jwt_validator



class CustomException(Exception):
    http_code: int
    code: str
    message: str

    def __init__(self, http_code: int = None, code: str = None, message: str = None):
        self.http_code = http_code if http_code else 500
        self.code = code if code else str(self.http_code)
        self.message = message


minio_router = APIRouter()


@minio_router.post("/upload", response_model=UploadFileResponse, dependencies=[Depends(jwt_validator)], status_code=status.HTTP_201_CREATED)
async def upload_file_to_minio(file: UploadFile = File(...)):
    try:
        data = file.file.read()
        file_name = " ".join(file.filename.strip().split())
        minio_instance = MinioHandler()

        minio_instance.put_object(
            file_name=file_name,
            file_data=BytesIO(data),
            content_type=file.content_type
        )

        return {
            "bucket_name": minio_instance.bucket_name,
            "file_name": file_name,
            "url": minio_instance.minio_url
        }
    except CustomException as e:
        raise e
    except Exception as e:
        if e.__class__.__name__ == 'MaxRetryError':
            raise CustomException(http_code=400, code='400',
                                  message='Can not connect to Minio')
        raise CustomException(code='999', message='Server Error')
