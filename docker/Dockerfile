
FROM python:3.13

WORKDIR /code
ENV PATH /root/.local/bin:$PATH

RUN python3 -m pip install --user pipx uvicorn["standard"]
RUN python3 -m pipx ensurepath

RUN pipx install poetry
COPY poetry.lock poetry.toml pyproject.toml /code/
RUN poetry install --no-interaction --no-root --without dev

COPY . .

CMD ["poetry", "run", "uvicorn", "forecasting.clients.api:app", "--workers", "3", "--host", "0.0.0.0", "--port", "80"]uvicorn
