from pydantic import BaseModel

class UploadFileResponse(BaseModel):
    bucket_name: str
    file_name: str
    url: str