FROM python:3.9

# 
WORKDIR /code/src

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./src /code/src

# 
CMD ["python3", "main.py"]
#CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "5011"]
