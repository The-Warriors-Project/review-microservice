import json
from datetime import datetime

from fastapi import FastAPI, Response, status, Request
from fastapi.openapi.models import Response
from fastapi.responses import JSONResponse

from review_resource import ReviewResource

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


@app.post("/api/v1/reviews")
async def get_reviews_by_book_id(request: Request):
    error = False
    try:
        data = await request.json()
        result = ReviewResource.create_review(data["book_id"], data["review_text"], data["user_id"], data["score"])
    except Exception as e:
        result = {
            "status": "Invalid Key Error",
            "body": e
        }
        print("got an error")
        error = True

    if error:
        return JSONResponse(content=json.loads(json.dumps(result, sort_keys=True, default=str)),
                            status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return JSONResponse(content=json.loads(json.dumps(result, sort_keys=True, default=str)),
                            status_code=status.HTTP_200_OK)


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
        return JSONResponse(content='NOT FOUND',
                            status_code=status.HTTP_404_NOT_FOUND)
