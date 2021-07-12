FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    libaio1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "sword.wsgi:application"]