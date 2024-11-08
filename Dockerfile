FROM python:3-alpine

# Встановлюємо необхідні залежності для компіляції Python пакетів
RUN apk add --no-cache build-base gcc musl-dev libffi-dev openssl-dev python3-dev unixodbc-dev

# Встановлюємо ODBC драйвер для MSSQL
RUN curl -o /etc/apk/keys/microsoft.asc https://packages.microsoft.com/keys/microsoft.asc && \
    echo "https://packages.microsoft.com/alpine/3.14/prod" >> /etc/apk/repositories && \
    apk update && \
    ACCEPT_EULA=Y apk add --no-cache msodbcsql18

# Додаємо код у контейнер
ADD . /code
WORKDIR /code

# Встановлюємо Gunicorn та Python залежності
RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install -r requirements.txt
