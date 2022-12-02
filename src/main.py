import json
from datetime import datetime

from fastapi import FastAPI, Response, status, Request
from fastapi.openapi.models import Response
from fastapi.responses import JSONResponse

from review_resource import ReviewResource

# from db_util import check_db_connection

app = FastAPI()


@app.get("/api/v1/reviews/health")
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
        print("theres an error")
        rsp = Response(json.dumps(result, sort_keys=True, default=str), status_code=status.HTTP_400_BAD_REQUEST)
    if result:
        print("theres result")
        print(type(result))
        print(type(json.dumps(result, sort_keys=True, default=str)))
        print(type(json.loads(json.dumps(result, sort_keys=True, default=str))))
        x = json.loads(json.dumps(result, sort_keys=True, default=str))
        # rsp = Response()
        # rsp.json(result)
        print(x)
        rsp = Response(result, status_code=status.HTTP_200_OK)
    else:
        print("theres none")
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


@app.post("/api/v1/reviews")
async def get_reviews_by_book_id(request: Request):
    error = False
    try:
        data1 = await request.body()
        print(data1)
        data = await request.json()
        result = ReviewResource.create_review(data["book_id"], data["review_text"], data["user_id"], data["score"])
    except Exception as e:
        result = {
            "status": "Invalid Key Error",
            "body": e
        }
        print("got an error")
        error = True
    return return_result(result, error)


@app.get("/api/v1/reviews")
def get_reviews_by_book_id(request: Request):
    error = False
    book_id, user_id = None, None
    if 'book_id' in request.query_params:
        book_id = request.query_params['book_id']
    if 'user_id' in request.query_params:
        user_id = request.query_params['user_id']
    if book_id and user_id:
        result = ReviewResource.get_by_book_and_user_id(book_id, user_id)
    elif book_id:
        result = ReviewResource.get_by_book_id(book_id)
    elif user_id:
        result = ReviewResource.get_by_user_id(user_id)
    else:
        result = ReviewResource.get_all_reviews()

    if result:
        return JSONResponse(content=json.loads(json.dumps(result, sort_keys=True, default=str)),
                            status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content=json.loads(json.dumps(result, sort_keys=True, default=str)),
                            status_code=status.HTTP_404_NOT_FOUND)
