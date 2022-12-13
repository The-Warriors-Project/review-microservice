import json
from datetime import datetime

from fastapi import FastAPI, Response, status, Request

from review_resource import ReviewResource
from reviews_endpoint import reviews_router

from src.middleware_sns import list_topics, publish_message

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


@app.middleware("http")
async def some_middleware_test_call(request: Request, call_next):
    ############################
    # put your "before request" stuff here
    # gets executed before every single Request
    print("before")
    for topic in list_topics():
        print(topic)
    ##########################
    # Don't change this
    response = await call_next(request)

    ############################
    # put your "After request" stuff here
    # gets executed after every single Request
    print(request.method)
    if request.method == "POST":
        msg = "this is a test message"
        subject = "this is a test subject"
        message_id = publish_message(msg, subject)
        print(message_id)
    ################################################

    return response
