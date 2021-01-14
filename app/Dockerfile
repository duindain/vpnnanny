FROM tiangolo/uvicorn-gunicorn-starlette:python3.8-alpine3.10
WORKDIR /app
COPY requirements.txt requirements.txt
COPY app/scripts/* /
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["entry-point.sh"]

RUN apk --no-cache add curl

COPY . /app
