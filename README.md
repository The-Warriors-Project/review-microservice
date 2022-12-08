# F22-Starter-Microservice

## Introduction

This is the Reviews Microservice for the Book Project. This Microservice has been set up on an EC2 instance and is running within a Docker container. We have provided instructions below to set up the project on your local machine.

### Steps to run the program locally (Within a Docker Container)

1. Make sure you have Docker CLI set up for your OS. We are using [Docker with Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04)

2. If you have not already created a Docker image, run the following command within the cloned repo:
`docker build -t myimage .`

3. After you have created your Docker image, you can launch the container with the following command within the cloned repo:
`docker run -d --name mycontainer -p 5011:5011 myimage`  

4. Make sure the AWS RDS instance is on.

### Steps to run the program locally (Without Docker Container)

1. Install the requirements file 
`pip install -r requirements.txt` 

2. Make sure the AWS RDS instance is on.

3. Run the command to activate the program 
```
cd src/
python3 main.py
```
## Endpoints 

Check out the documentation for this microservice here - http://3.82.245.34:5011/docs#/

Here is a brief list of endpoints:

- POST requests to /api/v1/reviews must include JSON format with keys book_id, username, review_text, score

- GET requests to /api/v1/reviews can include parameters for user_id, book_id, or both (primarily used for testing)

- GET requests to /api/v1/reviews/book_id/{book_id} and /api/v1/reviews/username/{username}

- PUT requests to /api/v1/reviews/{username}  


