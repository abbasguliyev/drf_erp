###################
Installment And Run
###################

Proyekti development-də run etmək üçün settings.py file-da __PRODUCTION__ dəyişənini False etmək lazımdır.

Dockersiz run etmək
-------------------

cd kodaze

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

Proyekti docker-siz run edərkən celery-ni run etmək üçün aşağıdakı komandanı terminalda run etmək lazımdır.
celery -A core worker --beat --scheduler django --loglevel=info

Docker ilə run etmək
--------------------

docker-compose build

docker-compose run --rm web python3 manage.py migrate

docker-compose run --rm web python3 manage.py createsuperuser

docker-compose up

Docker ilə run edərkən celery avtomatik run olur.
