import random
from datetime import datetime
from minio import Minio
from decouple import config

MINIO_URL = config["minio_url"]
MINIO_ACCESS_KEY = config["minio_access_key"]
MINIO_SECRET_KEY = config["minio_secret_key"]

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
        except Exception as e:
            print(f'Exception: {e}')
            return False

    def put_object(self, file_data, file_name, content_type):
        try:
            datetime_prefix = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            object_name = f"{datetime_prefix}___{file_name}"
            while self.check_file_name_exists(bucket_name=self.bucket_name, object_name=object_name):
                random_prefix = random.randint(1, 1000)
                object_name = f"{datetime_prefix}___{random_prefix}___{file_name}"
            self.client.put_object(bucket_name=self.bucket_name, object_name=object_name,
                                   data=file_data, content_type=content_type, length=-1, part_size=10*1024*1024)
            url = self.presigned_get_object(bucket_name=self.bucket_name, object_name=object_name)            
        except Exception as e:
            raise Exception(e)
