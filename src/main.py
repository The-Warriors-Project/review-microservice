import uvicorn


def start_reviews_microservice():
    uvicorn.run(  # TODO: change later localhost..
        app="app:app",
        host="0.0.0.0",
        port=5011
    )


if __name__ == "__main__":
    start_reviews_microservice()
