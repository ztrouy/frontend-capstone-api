#!/bin/bash

rm db.sqlite3
rm -rf ./gamegaugeapi/migrations
python manage.py migrate
python manage.py makemigrations gamegaugeapi
python manage.py migrate gamegaugeapi
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata genres
python manage.py loaddata platforms
python manage.py loaddata games
python manage.py loaddata groups
python manage.py loaddata game_genres
python manage.py loaddata game_platforms
python manage.py loaddata user_games
python manage.py loaddata user_groups

