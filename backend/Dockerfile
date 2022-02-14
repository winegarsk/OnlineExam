FROM nginx:1.13
COPY conf /etc/nginx/conf.d/default.conf
FROM python:3.9-slim-buster
ENV FLASK_APP=/backend/src/app/__init__.py
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY . .

RUN pip3 install -r requirements.txt
RUN pip3 install requests
RUN pip3 install pipenv
RUN pip3 install psycopg2-binary
RUN pipenv install sqlalchemy psycopg2-binary

EXPOSE 5000
WORKDIR /src

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]



