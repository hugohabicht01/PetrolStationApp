FROM python:3.9

RUN python -m pip install --upgrade pip
RUN python -m pip install pipenv
RUN pipenv sync --dev

EXPOSE 80

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
