FROM python:3.7-alpine@sha256:c9c2d6f97a00b211def3818830883495417e3b1fd34783ce6135c5fc03b5ee87

COPY ./requirements.txt /app/

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install -r requirements.txt

WORKDIR /app

COPY . /app/

EXPOSE 8000

# CMD python manage.py runserver 0.0.0.0:8000