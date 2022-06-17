#!/bin/bash

docker stop atk-gunicorn
docker rm atk-gunicorn

docker run -it -p 8000:8000 --name atk-gunicorn --mount type=bind,source=/home/art/atk/atkdjango/atk.sqlite,target=/app/atkdjango/atk.sqlite atk-gunicorn:latest sh
#docker run -it -p 8000:8000 --name atk-gunicorn atk-gunicorn:latest sh

