# DRF ERP

## Install
git clone https://github.com/abbasguliyev/kodazeERP.git
## Configuration
create .env file inside src folder, then copy and paste the contents of the env file. 
## Run with Docker
docker-compose build \
docker-compose run --rm web python3 manage.py migrate
docker-compose run --rm web python3 manage.py createsuperuser
docker-compose up

## Run without Docker
cd src \
python manage.py migrate \
python manage.py createsuperuser \
python manage.py runserver \