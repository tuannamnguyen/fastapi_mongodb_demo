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
class User(Document):
    fullname = fields.StringField(required=True)
    username = fields.StringField(unique=True, required=True)
    password = fields.StringField(required=True)

    class Meta:
        collection_name = "users"