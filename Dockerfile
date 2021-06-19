FROM python:3.9

RUN python -m pip install --upgrade pip
RUN python -m pip install pipenv

COPY ./Pipfile /Pipfile
COPY ./Pipfile.lock /Pipfile.lock

RUN pipenv sync --dev

EXPOSE 80

COPY ./app /app

CMD ["pipenv","run", "serve"]
