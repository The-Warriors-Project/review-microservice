# F22-Starter-Microservice

## Introduction

This is the Reviews Microservice for the Book Project.

### Steps to run the program locally

1. Install the requirements file 
`pip install -r requirements.txt` 

2. Make sure the AWS RDS instance is on.

3. Run the command to activate the program 
```
cd src/
uvicorn main:app --host 0.0.0.0 --port 5011
```
## Endpoints 

- POST requests to /api/v1/reviews must include JSON format with keys book_id, user_id, review_text, score

- GET requests to /api/v1/reviews can include parameters for user_id, book_id, or both

