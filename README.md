# Theatre API

API service for theatre management written on DRF

## Features
+ JWT authentication 
+ Admin panel /admin/
+ Documentation is located at /api/doc/swagger/
+ Managing reservations and tickets
+ Creating plays with genres and actors
+ Filtering plays and performances

## Technologies Used
+ **Backend:** Python, Django
+ **Database:** postgresql

## Installing using GitHub
Install PostgresSQL and create db

```angular2html
git clone https://github.com/Liliyakhu/theatre_API.git
cd theatre_API
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
set POSTGRES_HOST=<your db hostname>
set POSTGRES_DB=<your db name>
set POSTGRES_USER=<your db username>
set POSTGRES_PASSWORD=<your db user password>
set POSTGRES_PORT=<your db port>
set SECRET_KEY=<your secret key>
python manage.py migrate
python manage.py runserver
```
## Run with docker
Docker should be installed
```angular2html
docker compose build
docker compose up
```

## Getting access
* create user via /api/user/register/
* get access token via /api/user/token



## Screenshots
### Register:
![Screenshot from 2025-05-21 13-57-54](https://github.com/user-attachments/assets/e7ec2a45-bb06-4eab-904f-26b4084ed75a)

### Receive your token:
![Screenshot from 2025-05-21 13-59-27](https://github.com/user-attachments/assets/321a54ee-2cb5-4b63-bdad-5c441e5344fc)### Use theatre app:

### Ready to use theatre app
![Screenshot from 2025-05-21 14-00-52](https://github.com/user-attachments/assets/bb4c50ec-d252-441f-a220-7c59d8632ffd)