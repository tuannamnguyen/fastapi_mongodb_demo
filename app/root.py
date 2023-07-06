from fastapi import FastAPI
from fastapi_redis_cache import FastApiRedisCache
from fastapi.responses import HTMLResponse
from app.students.student_router import student_router
from app.users.user_router import user_router
from app.minio.minio_router import minio_router
from app.websocket import websocket_router
from decouple import config
from starlette.middleware.cors import CORSMiddleware

REDIS_URL = config("redis_url")

app = FastAPI()
app.include_router(student_router, prefix="/students", tags=["Students"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(minio_router, tags=["MinIO"])
app.include_router(websocket_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
def startup():
    redis_cache = FastApiRedisCache()
    redis_cache.init(
        host_url=REDIS_URL,
        prefix="myapi-cache",
        response_header="X-MyAPI-Cache",
    )


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def root():
    return HTMLResponse(html)
