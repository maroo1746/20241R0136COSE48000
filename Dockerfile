FROM python:3.9 AS builder
WORKDIR /bulid

COPY requirements_all.txt requirements.txt
COPY ./.pip ~/.pip

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

FROM python:3.9-slim AS app
WORKDIR /code

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY .env /code/.env
COPY ./app /code/app
EXPOSE 8000

