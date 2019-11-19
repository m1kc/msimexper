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
RUN poetry config
RUN echo "[settings]\nvirtualenvs.create=false\n\n[repositories]\n" > /root/.config/pypoetry/config.toml

COPY pyproject.toml ./
COPY poetry.lock ./
RUN poetry install

CMD ["python", "/usr/django/app/server.py"]

ENV DJANGO_SETTINGS_MODULE msimexper.settings
ENV DJANGO_APP=msimexper

ENV GUNICORN_CMD_ARGS "-t 120 -w4"

ENV DJANGO_MANAGEMENT_ON_START "migrate"

COPY . /usr/django/app
