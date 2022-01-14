FROM nginx:1.13-alpine
WORKDIR /nginx
COPY conf /etc/nginx/conf.d/default.conf
FROM python:3.7-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
RUN pip install netcat
RUN pip3 install -r ./requirements.txt
ENTRYPOINT ["./entrypoint.sh"]


