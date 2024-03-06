FROM python:3.10-alpine

RUN apk update && apk add bash
RUN apk add nano
RUN mkdir /app
RUN mkdir -p /logs/auth

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8042

CMD ["gunicorn", "app:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8001"]
