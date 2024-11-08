FROM python:3-alpine

# Встановлюємо необхідні залежності для компіляції Python пакетів
RUN apk add --no-cache build-base gcc musl-dev libffi-dev openssl-dev python3-dev mariadb-connector-c-dev

# Додаємо код у контейнер
ADD . /code
WORKDIR /code

# Встановлюємо Gunicorn та Python залежності
RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install -r requirements.txt
