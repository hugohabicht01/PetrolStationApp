FROM python:3.9

RUN pip install pipenv

EXPOSE 8000

COPY ./app /app
COPY ./Pipfile /Pipfile
COPY ./Pipfile.lock /Pipfile.lock
COPY ./.env /.env

RUN pipenv install


CMD ["pipenv", "run", "dev"]

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]