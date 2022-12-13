import json
from datetime import datetime

from fastapi import FastAPI, Response, status, Request
from starlette.types import Message

from review_resource import ReviewResource
from reviews_endpoint import reviews_router
from src.middleware_sns import publish_message

app = FastAPI()
app.include_router(reviews_router)


@app.get("/api/v1/reviews/health")
def get_health():
    try:
        connection = ReviewResource._get_connection()
        t = str(datetime.now())
        if connection:
            db_connection_status = True
            status_code = status.HTTP_200_OK
            health = "Good"
        else:
            db_connection_status = False
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            health = "Not good"

    except:
        db_connection_status = False
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        health = "Not good"
        t = str(datetime.now())

    msg = {
        "name": "Reviews-Microservice",
        "health": health,
        "DB connection": db_connection_status,
        "at time": t
    }

    result = Response(json.dumps(msg), status_code=status_code)

    return result


async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {"type": "http.request", "body": body}

    request._receive = receive


async def get_body(request: Request) -> bytes:
    body = await request.body()
    await set_body(request, body)
    return body


@app.middleware("http")
async def some_middleware_test_call(request: Request, call_next):
    await set_body(request, await request.body())
    params = dict(json.loads((await get_body(request)).decode('utf-8')))
    response = await call_next(request)
    if request.method == "POST":
        msg = params["username"] + "#" + params["title"] + "#" + params["email"]
        subject = "review_confirmation_subject"
        publish_message(msg, subject)
    return response
