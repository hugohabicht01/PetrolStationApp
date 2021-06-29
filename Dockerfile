FROM python:3.9

ENV APP_HOME /app_home

WORKDIR ${APP_HOME}
RUN python -m pip install --upgrade pip
RUN python -m pip install pipenv

COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock

RUN pipenv sync --dev --system

EXPOSE 80

COPY ./app ./app
COPY ./.env ./.env

CMD ["pipenv","run", "serve"]
