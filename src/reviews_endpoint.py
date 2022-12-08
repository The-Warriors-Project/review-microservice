import json
from datetime import datetime

from fastapi import APIRouter, FastAPI, Response, status, Request
from fastapi.openapi.models import Response
from fastapi.responses import JSONResponse
import uvicorn

from review_resource import ReviewResource


reviews_router = APIRouter(prefix='/api/v1/reviews')


@reviews_router.get(path='/username/{username}', status_code=status.HTTP_200_OK, operation_id='get_all_reviews_by_user_id')
def get_reviews_by_user_id(username: str):
    """

    :param username: username
    :return: return all reviews for a given username
    """
    result = ReviewResource.get_by_user_id(username)
    if result:
        return JSONResponse(content=json.loads(json.dumps(result, sort_keys=True, default=str)),
                            status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content='NOT FOUND',
                            status_code=status.HTTP_404_NOT_FOUND) 



@reviews_router.get(path='/book_id/{book_id}', status_code=status.HTTP_200_OK, operation_id='get_all_reviews_by_book_id')
def get_reviews_by_book_id_path(book_id: int):
    """

    :param book_id: book id
    :return: return all reviews for a given book_id
    """
    result, avg  = ReviewResource.get_by_book_id(book_id)
    msg = { 
        "reviews": result, 
        "average_score": avg
    }
    if result:
        return JSONResponse(content=json.loads(json.dumps(msg, sort_keys=True, default=str)),
                            status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content='NOT FOUND',
                            status_code=status.HTTP_404_NOT_FOUND) 
    
@reviews_router.put("/{username}")
async def remove_reviews(username: str, request: Request):
    try:
        data = await request.json() 
        result = ReviewResource.remove_reviews_for_user(username, data["disabled"])
    except:
        result = None #Failure        

    msg = {
        "status" : "Success"
    }

    if result:
        return JSONResponse(content=json.loads(json.dumps(msg, sort_keys=True, default=str)),
                            status_code=status.HTTP_200_OK)
    else:
        msg["status"] = "Failure" 
        return JSONResponse(content=msg,
                            status_code=status.HTTP_404_NOT_FOUND) 



@reviews_router.post("")
async def get_reviews_by_book_id(request: Request):
    """
    :param book_id: unique book_id 
    :param review_text: user's review 
    :param username: unique username 
    :param score: float value between 0-5 
    """
    error = False
    try:
        data = await request.json()
        result = ReviewResource.create_review(data["book_id"], data["review_text"], data["username"], data["score"])
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


@reviews_router.get("")
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


