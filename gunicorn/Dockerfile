# Dockerfile

#FROM python:3.7-buster
#FROM python:3.8-alpine
FROM alpine
RUN apk add --no-cache py3-django py3-pillow py3-dateutil py3-gunicorn

# alpine compile python modules
#RUN apk add --no-cache --virtual build-deps build-base python3-dev py3-pip 
#RUN apk add --no-cache jpeg-dev zlib-dev
#RUN python3 -m pip install -U --force-reinstall pip
#COPY requirements.txt /
#RUN pip install -r /requirements.txt
#RUN apk del build-deps
#############################

EXPOSE 8000
STOPSIGNAL SIGTERM

WORKDIR /app/atkdjango
CMD /usr/bin/gunicorn --bind 0.0.0.0:8000 atkdjango.wsgi

