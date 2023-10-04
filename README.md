# FileUploderTest
PICASSO 

[![Python application](https://github.com/DerTod28/FileUploderTest/actions/workflows/python-app.yml/badge.svg)](https://github.com/DerTod28/FileUploderTest/actions/workflows/python-app.yml)

## Table of Contents
+ [About](#about)
    + [Prerequisites](#prerequisites)
+ [Getting Started](#getting-started)
    + [Quickstart with docker-compose](#quickstart)
    + [Testing](#testing)
+ [Management commands](#management-commands)

## About <a name = "about"></a>
Picasso File Uploader backend server

### Prerequisites <a name = "prerequisites"></a>
```
Python 3.11.6
Postgres (inside container)
Redis (inside container)
Celery (inside container)
```
```
docker v20+
docker-compose v1.27+
```

## Getting Started <a name = "getting-started"></a>
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Quickstart with docker-compose <a name = "quickstart"></a>

- Start conteinerized services
```
docker-compose up -d
```
- Installing dependencies
```
# Do it for the first time

pip install poetry

# Do it each time you would like to setup dependencies

poetry shell
poetry install

```
- Copying configs
```
cp example.env .env
```
- Start migrations
```
python manage.py migrate
```
- Create createsuperuser
```
python manage.py createsuperuser
```
- Start development server
```
python manage.py runserver
```
or run command
```
make run
```

Server will start on localhost:8000

docker-compose -f docker-compose.prod.yml up --build -d


## Management commands <a name = "management-commands"></a>

## Command-helpers for local development

- `make help` - display available commands
- `make run` - run local developer server
- `make qa` - run tests
- `make pep8` - run linter
- `make worker` - run celery workers with auto reload
- `make scheduler` - run celery beat scheduler
