from io import BytesIO

from decouple import config
from fastapi import HTTPException
from minio import Minio
from minio.error import S3Error
from starlette.responses import StreamingResponse

MINIO_URL = config("minio_url")
MINIO_ACCESS_KEY = config("minio_access_key")
MINIO_SECRET_KEY = config("minio_secret_key")


class MinioHandler():
    def __init__(self):
        self.minio_url = MINIO_URL
        self.access_key = MINIO_ACCESS_KEY
        self.secret_key = MINIO_SECRET_KEY
        self.bucket_name = "fastapi-minio"
        self.client = Minio(self.minio_url, access_key=self.access_key,
                            secret_key=self.secret_key, secure=False)
        self.make_bucket()

    def make_bucket(self) -> str:
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)
        return self.bucket_name

    def presigned_get_object(self, bucket_name: str, object_name: str):
        # Request URL expired after 7 days
        url = self.client.presigned_get_object(
            bucket_name=bucket_name, object_name=object_name)
        return url

    def check_file_name_exists(self, bucket_name: str, object_name: str) -> bool:
        try:
            self.client.stat_object(
                bucket_name=bucket_name, object_name=object_name)
            return True
        except S3Error:
            return False

    def put_object(self, file_data, file_name, content_type):
        object_name = f"{file_name}"
        if self.check_file_name_exists(bucket_name=self.bucket_name, object_name=object_name):
            raise HTTPException(
                status_code=409, detail="File already exists. Please rename the file and try again")
        self.client.put_object(bucket_name=self.bucket_name, object_name=object_name,
                               data=file_data, content_type=content_type, length=-1, part_size=10*1024*1024)
        return {
            "bucket_name": self.bucket_name,
            "file_name": object_name,
            "url": self.minio_url
        }

    def get_object(self, object_name):
        if self.check_file_name_exists(bucket_name=self.bucket_name, object_name=object_name):
            _file = self.client.get_object(
                self.bucket_name, object_name=object_name).read()
            return StreamingResponse(BytesIO(_file))
        raise HTTPException(status_code=404, detail="File not found")
