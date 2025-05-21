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

[//]: # (![Screenshot from 2024-12-04 22-50-13]&#40;https://github.com/user-attachments/assets/c4de94e1-47e6-4aef-a841-a40e01c3d2b6&#41;)
### Receive your token:

[//]: # (![Screenshot from 2024-12-04 22-51-12]&#40;https://github.com/user-attachments/assets/f726ec01-1250-40c6-b209-d2ccc64900ea&#41;)
### Use theatre app:

[//]: # (![Screenshot from 2024-12-04 22-55-25]&#40;https://github.com/user-attachments/assets/d54dbd9b-b469-4455-9212-72cbfe21034f&#41;)
