FROM python:3.11-slim-bookworm

# Выберите папку, в которой будут размещаться файлы проекта внутри контейнера
WORKDIR /usr/src/app

# Заведите необходимые переменные окружения
ENV DJANGO_SETTINGS_MODULE 'picasso.settings'
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV POETRY_VERSION=1.2.2

# Скопируйте в контейнер файлы, которые редко меняются
CMD chmod 777 picasso/deploy/initapp.sh
COPY picasso/deploy/initapp.sh initapp.sh

# Установите зависимости
RUN  mkdir -p /usr/src/app/public \
     && mkdir -p /usr/src/app/log \
     && pip install --upgrade pip --no-cache-dir \
     && pip install "poetry==$POETRY_VERSION"

COPY poetry.lock .
COPY pyproject.toml .

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Скопируйте всё оставшееся. Для ускорения сборки образа эту команду стоит разместить ближе к концу файла.
COPY manage.py .
COPY picasso/deploy/config.env  .env
COPY picasso picasso


ENV PYTHONPATH ${PYTHONPATH}:/usr/src/picasso

# Укажите, как запускать ваш сервис
ENTRYPOINT ["./initapp.sh"]