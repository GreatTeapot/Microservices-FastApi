FROM python:latest

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN ls -l /

RUN ls -l /app/docker/  # Проверка наличия файла app.sh

RUN chmod a+x /app/docker/*.sh

