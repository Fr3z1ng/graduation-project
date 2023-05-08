FROM python:3.10 as reduction_url_admin
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt requirements.txt ./
RUN pip install -r requirements.txt

ADD online ./online
ADD .env entrypoint.sh./
