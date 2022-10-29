# kodazeERP

## Install
git clone https://github.com/abbasguliyev/kodazeERP.git
## Run with Docker
docker-compose build \
docker-compose run --rm web python3 manage.py migrate
docker-compose run --rm web python3 manage.py createsuperuser
docker-compose up

## Run without Docker
cd kodaze \
python manage.py migrate \
python manage.py createsuperuser \
python manage.py runserver \

## Doc
http://localhost:8000/docs/html/index.html