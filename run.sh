#!/bin/bash

docker stop atk
docker rm atk

docker run -d -p 8000:8000 --name atk --mount type=bind,source=/home/art/atk/atkdjango,target=/app/atkdjango atk:latest

