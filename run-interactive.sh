#!/bin/bash

docker stop atk
docker rm atk

docker run -it -p 8000:8000 --name atk --mount type=bind,source=/home/art/atk/atkdjango,target=/app/atkdjango --mount type=bind,source=/home/art/atk/pics,target=/app/atkdjango/storage/pics atk:latest bash

