#!/bin/bash

docker stop gunicorn
docker rm gunicorn

docker run -d -p 8000:8000 --name gunicorn --mount type=bind,source=/home/art/atk/atkdjango,target=/app/atkdjango --mount type=bind,source=/home/art/atk/pics,target=/app/atkdjango/storage/pics gunicorn:latest

