# Forecast App


## How to Run the Application
## Prerequisites

It's recommended to use `pyenv` or `asdf` to manage Python versions.
This guide uses `asdf`: [https://asdf-vm.com/](https://asdf-vm.com/), but `pyenv` is also a valid option.

## Quick Setup
Using `make` is it more quick to setup the environment. By the way, in the other section I have explained how to do it manually.

```sh
Usage:
  make setup       - Set up the environment (install dependencies, pre-commit hooks, etc.)
  make test        - Run all tests
  make coverage    - Run tests with coverage
  make docker-up   - Start Docker containers (use -d to run in detached mode)
  make docker-build - Build and start Docker containers
  make docker-stop - Stop and remove Docker containers
  make api         - Start the forecast API
  make ui          - Start the Streamlit UI
  make stop-ui     - Stop the Streamlit UI
  make clean       - Clean up the environment (remove .venv and other generated files)
  make help        - Show this help message
```

## Setting Up the Environment (Optional)

If you want to use a virtual environment (you must do):

```sh
python -m venv .venv
source .venv/bin/activate
pip install pipx pre-commit
pipx install poetry  # Or use the official Poetry installer
poetry install # this will install tool.scripts
pre-commit install
```

## Running Tests
```sh
pytest  # all tests
pytest -m integration  # Integration tests
```

## Running the Clients
Running the Streamlit UI.
```sh
forecast-ui
```
it isn't a very interesting client, but the idea was serving the app with some clients

Running the API (FastAPI) [the important]
```sh
forecast-api
```
If the port is already in use, you can free it with:

```sh
lsof -i:<port>  # Identify the process
kill <PID>  # Terminate the process
```

Then, access the API documentation at:

http://127.0.0.1:8000/docs. The endpoint has an example input to run.

## Debugging in VS Code
To debug the API in VS Code, press F5 and navigate to http://127.0.0.1:8000/docs.

## Running with Docker
```sh
docker compose -f docker/docker-compose.yml up -d --build
```

Then, navigate to the API at: http://0.0.0.0:8002/docs
