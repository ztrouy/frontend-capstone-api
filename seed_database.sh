#!/bin/bash

rm db.sqlite3
rm -rf ./gamegaugeapi/migrations
python manage.py migrate
python manage.py makemigrations gamegaugeapi
python manage.py migrate gamegaugeapi
python manage.py loaddata users
python manage.py loaddata tokens

