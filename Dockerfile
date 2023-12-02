FROM python:3.10 as setup_and_test
ENV ENV_NAME=staging
WORKDIR /flask-app
COPY app ./app
COPY api.py .
COPY requirements.txt .
COPY entrypoint.sh .
COPY logging_config.yaml .

RUN pip install gunicorn
RUN pip install -r requirements.txt

FROM setup_and_test as stage
EXPOSE 5000
ENV ENV_NAME=staging
ENV FLASK_APP=api
ENV GUNICORN_WORKERS=4

RUN ["chmod", "+x", "./entrypoint.sh"]
ENTRYPOINT ["./entrypoint.sh"]
