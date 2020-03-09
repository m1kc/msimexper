# EXPERIMENTAL!
# Not for production use.

FROM alang/django:2.1-python3

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        mariadb-client \
        nano \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml ./
COPY poetry.lock ./
RUN poetry install

ENV DJANGO_SETTINGS_MODULE msimexper.settings
ENV DJANGO_APP=msimexper

ENV DJANGO_MANAGEMENT_ON_START "migrate"

COPY . /usr/django/app
