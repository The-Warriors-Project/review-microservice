import json
from datetime import datetime

from fastapi import FastAPI, Response, status, Request
from fastapi.openapi.models import Response

from review_resource import ReviewResource

# from db_util import check_db_connection

app = FastAPI()


@app.get("/api/health")
def get_health():
    t = str(datetime.now())
    # db_connection = check_db_connection()
    msg = {
        "name": "Review-Microservice",
        "health": "Good",
        "at time": t
    }
    result = Response(json.dumps(msg), status_code=status.HTTP_200_OK)
    return result


def return_result(result, error=False):
    if error:
        rsp = Response(json.dumps(result, sort_keys=True, default=str), status_code=status.HTTP_400_BAD_REQUEST)
    if result:
        rsp = Response(json.dumps(result, sort_keys=True, default=str), status_code=status.HTTP_200_OK)
    else:
        rsp = Response(content="NOT FOUND", status_code=status.HTTP_404_NOT_FOUND)
    return rsp


# ENDPOINT FOR TESTING ONLY
@app.get('/api/reviews/{book_id}')
def get_book_by_id(book_id: int):
    result = ReviewResource.get_by_book_id(book_id)

    if result:
        rsp = Response(json.dumps(result, sort_keys=True, default=str), status_code=status.HTTP_200_OK)
    else:
        rsp = Response(content="NOT FOUND", status_code=status.HTTP_404_NOT_FOUND)

    return rsp


@app.get("/api/v1/reviews")
def get_reviews_by_book_id(request: Request):
    error = False
    data = request.json()
    try:
        result = ReviewResource.create_review(data["book_id"], data["review_text"], data["user_id"], data["score"])
    except Exception as e:
        result = {
            "status": "Invalid Key Error",
            "body": e
        }
        error = True
    return return_result(result, error)


@app.post("/api/v1/reviews")
def get_reviews_by_book_id_post(request: Request):
    error = False
    book_id = request.query_params['book_id']
    user_id = request.query_params['user_id']
    if book_id and user_id:
        result = ReviewResource.get_by_book_and_user_id(book_id, user_id)
    elif book_id:
        result = ReviewResource.get_by_book_id(book_id)
    elif user_id:
        result = ReviewResource.get_by_user_id(user_id)
    else:
        result = ReviewResource.get_all_reviews()

    return return_result(result, error)
