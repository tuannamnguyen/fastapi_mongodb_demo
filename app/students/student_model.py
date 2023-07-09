from umongo.frameworks import MotorAsyncIOInstance
from decouple import config
from umongo import validate, Document, fields
import motor.motor_asyncio


DB_CONNECTION_STRING = config("db_connection_string")

# Connect to DB
client = motor.motor_asyncio.AsyncIOMotorClient(DB_CONNECTION_STRING)
db = client['demoapp']
instance = MotorAsyncIOInstance(db)


@instance.register
class Student(Document):
    student_id = fields.IntegerField(unique=True)
    fullname = fields.StringField()
    email = fields.EmailField()
    gender = fields.StringField(validate=validate.Regexp(
        r"(?:m|M|male|Male|f|F|female|Female|FEMALE|MALE|Non-binary)$"))
    major = fields.StringField()
    year = fields.IntegerField(validate=validate.Range(min=0, max=4))
    gpa = fields.FloatField(validate=validate.Range(min=0, max=4))

    class Meta:
        collection_name = "students"

@instance.register
class StudentUpdate(Document):
    fullname = fields.StringField(allow_none=True)
    email = fields.EmailField(allow_none=True)
    gender = fields.StringField(validate=validate.Regexp(
        r"(?:m|M|male|Male|f|F|female|Female|FEMALE|MALE|Non-binary)$"), allow_none=True)
    major = fields.StringField(allow_none=True)
    year = fields.IntegerField(validate=validate.Range(min=0, max=4), allow_none=True)
    gpa = fields.FloatField(validate=validate.Range(min=0, max=4), allow_none=True)

    class Meta:
        collection_name = "students"

