# bongo-restaurant-api

This project is fully dockerized, so just run those commands
```commandline
    sudo docker-compose build
    sudo docker-compose up
```
Note - All makemigrations and migrate commands are inside docker-compose.yml file
*** 

if you need to create superusers use this command
```commandline
    sudo docker-compose run web python manage.py createsuperuser
```

implemented black, flake8 & isort into this project


