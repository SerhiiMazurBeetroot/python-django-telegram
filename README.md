# Python Django Telegram

## What's inside

<p align="center">
    <img alt="Docker" src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white">
    <img alt="Python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
    <img alt="pgAdmin" src="https://img.shields.io/badge/pgAdmin-316192?style=for-the-badge&logo=Amazon%20DynamoDB&logoColor=white">
    <img alt="Postgres" src="https://img.shields.io/badge/Postgres-4169E1?style=for-the-badge&logo=postgresql&logoColor=white">
</p>

## APIs used

<p align="center">
    <img alt="Telegram" src="https://img.shields.io/badge/Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white">
    <img alt="openweathermap" src="https://img.shields.io/badge/openweathermap-%23ED8B00?style=for-the-badge&logo=weather&logoColor=white">
    <img alt="jokeapi" src="https://img.shields.io/badge/jokes-darkblue?style=for-the-badge&logo=jokes&logoColor=white">
    <img alt="NBU" src="https://img.shields.io/badge/NBU-0AC18E?style=for-the-badge&logo=jokes&logoColor=white">
</p>

## Requirements

1. Install Docker v20.10+ for your platform:

   - [Linux](https://docs.docker.com/engine/installation)
   - [Docker for Mac](https://docs.docker.com/engine/installation/mac)
   - [Docker for Windows](https://docs.docker.com/engine/installation/windows)

2. For Linux additionally install [Docker Compose](https://docs.docker.com/compose/install) v1.29+

## Setup

1. Create .env file

```bash
cp .env.example .env
```

2. Enter your keys:

```
TELEGRAM_BOT_API_KEY=
OPENWEATHERMAP_TOKEN=
```

3. Build the images and spin up the containers:

```bash
docker compose up -d
```

4. Visit:

- [Django](http://localhost:8000/)
- [PgAdmin](http://localhost:8088/)

5. Connect to py_django terminal

```bash
docker exec -it py_django bash
```

6. Start bot

```bash
python manage.py telegram
```

## Development

1. Connect to py_django terminal

```bash
docker exec -it py_django bash
```

2. Creating an admin user

```bash
python manage.py createsuperuser
```

3. Working with models:

```bash
python manage.py makemigrations

python manage.py migrate
```

## PgAdmin

1. Visit:

- [PgAdmin](http://localhost:8088/)

2. Login

```
admin@example.com
postgres
```

3. Add new Server:

```
name: py_db
host name/address: py_db
username: python
password: python
```

## FAQ

1. [Django Documentation](https://docs.djangoproject.com/en/5.0/intro/tutorial01/)
