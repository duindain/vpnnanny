FROM tiangolo/uvicorn-gunicorn-starlette:python3.8-alpine3.10
WORKDIR /app
COPY requirements.txt requirements.txt
COPY app/scripts/entry-point.sh /
COPY app/scripts/run.sh /

RUN pip install --no-cache-dir -r requirements.txt

RUN sh /entry-point.sh

RUN apk --no-cache add curl

COPY . /app
