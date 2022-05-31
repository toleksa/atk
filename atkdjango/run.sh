#!/bin/sh

python3 /app/atkdjango/manage.py runserver 0:8000 2>&1 | tee /app/atkdjango/atkdjango.log

