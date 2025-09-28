FROM python:3.13.3

RUN pip install --no-cache-dir poetry

WORKDIR /code

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

COPY . .

CMD ["python", "main.py"]