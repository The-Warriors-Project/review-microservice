from flask import Flask, Response, request
from datetime import datetime
import json
from review_resource import ReviewResource 
from flask_cors import CORS

# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(app)


@app.get("/api/v1/reviews/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "Review-Microservice",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result

def return_result(result):
    if result:
        rsp = Response(json.dumps(result, sort_keys=True, default=str), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


#ENDPOINT FOR TESTING ONLY
@app.route("/api/reviews/<book_id>", methods=["GET"])
def get_book_by_id(book_id):

    result = ReviewResource.get_by_book_id(book_id)

    if result:
        rsp = Response(json.dumps(result, sort_keys=True, default=str), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp

@app.route("/api/v1/reviews", methods=["GET", "POST"])
def get_reviews_by_book_id():
    if request.method == "POST":
        data = request.get_json()
        result = ReviewResource.create_review(data["book_id"], data["review_text"], data["user_id"], data["score"])
    elif request.args.get("book_id") and request.args.get("user_id"):
        book_id = request.args.get("book_id")
        user_id = request.args.get("user_id")
        result = ReviewResource.get_by_book_and_user_id(book_id,user_id)
    elif request.args.get("book_id"):
        book_id = request.args.get("book_id")
        result = ReviewResource.get_by_book_id(book_id)
    elif request.args.get("user_id"):
        user_id = request.args.get("user_id")
        result = ReviewResource.get_by_user_id(user_id)
    else:
        result = ReviewResource.get_all_reviews()

    return return_result(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)

