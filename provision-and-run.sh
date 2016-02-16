#!/usr/bin/env bash

# Wait for the database to be ready
# then run the development server

start=${SECONDS}
echo "Waiting for database ..."
while ! nc -w 1 -z db 5432; do
    if [ "$(expr ${SECONDS} - ${start})" -gt "5" ]; then
        echo "Giving up after 5 seconds"
        exit
    fi
    sleep 0.1
done
echo "Database ready"

python manage.py migrate --noinput
python manage.py runserver_plus 0.0.0.0:5000
