# syntax=docker/dockerfile:1

FROM python:3
RUN mkdir /app
ENV PYTHONUNBUFFERED=1

WORKDIR /code

EXPOSE 8000
COPY requirements.txt /code/

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /code/   
# ENTRYPOINT ["python3"]
# CMD ["manage.py", "runserver", "0.0.0.0:8000", "src/app.py", "python"]

