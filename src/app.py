from fastapi import FastAPI, Response, status
from datetime import datetime
import json
from reviews_endpoint import reviews_router 
from review_resource import ReviewResource 

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
