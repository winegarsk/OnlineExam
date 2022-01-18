FROM nginx:1.13-alpine
COPY conf /etc/nginx/conf.d/default.conf
FROM python:3.9-alpine
ENTRYPOINT [ "entrypoint.sh" ]
ENV FLASK_APP=/backend/src/app/__init__.py
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY . .
RUN pip3 install -r requirements.txt
RUN pip3 install pipenv
RUN pip3 install psycopg2-binary
RUN pipenv install sqlalchemy psycopg2-binary
# RUN flask run -h 0.0.0.0

