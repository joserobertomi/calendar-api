docker compose up -d
docker exec -it dz01 python manage.py migrate 
docker exec -it dz01 python manage.py makemigrations calendar_api
docker exec -it dz01 python manage.py createsuperuser --username admin --email joserobertomi@outlook.com 