DOCKER_COMPOSE_FILE=docker/docker-compose.yml
PYTHON_REQUIRED_VERSION=3.13
PYTHON_INSTALLED_VERSION=$(shell python --version 2>&1 | awk '{print $$2}' | cut -d '.' -f 1,2)
# Verify if SO is macOS or Linux
ifeq ($(shell uname), Darwin)
    BROWSER=open  # Para macOS
else
    BROWSER=xdg-open  # Para Linux
endif

# Verify the python version
ifeq ($(shell echo "$(PYTHON_INSTALLED_VERSION) < $(PYTHON_REQUIRED_VERSION)" | bc), 1)
$(info ❌ Python version $(PYTHON_INSTALLED_VERSION) is not compatible. Please install Python $(PYTHON_REQUIRED_VERSION) or higher.)
$(error INVALID_PYTHON_VERSION)
endif

# Comando de ayuda
help:
	@echo "Usage:"
	@echo "  make setup       - Set up the environment (install dependencies, pre-commit hooks, etc.)"
	@echo "  make test        - Run all tests"
	@echo "  make coverage    - Run tests with coverage"
	@echo "  make docker-up   - Start Docker containers (use -d to run in detached mode)"
	@echo "  make docker-build - Build and start Docker containers"
	@echo "  make docker-stop - Stop and remove Docker containers"
	@echo "  make api         - Start the forecast API"
	@echo "  make ui          - Start the Streamlit UI"
	@echo "  make stop-ui     - Stop the Streamlit UI"
	@echo "  make clean       - Clean up the environment (remove .venv and other generated files)"
	@echo "  make help        - Show this help message"

.PHONY: setup
setup:
	@echo "🛠 Setting up environment..."
	@python -m venv .venv
	. .venv/bin/activate
	@pip install pipx pre-commit
	@pipx install poetry
	@poetry install
	@pre-commit install

.PHONY: test
test:
	@echo "🧪 Running tests..."
	@pytest
	@echo "✅ Tests completed."

.PHONY: integration-test
integration-test:
	@echo "🧪 Running tests..."
	@pytest -m integration
	@echo "✅ Tests completed."

.PHONY: coverage
coverage:
	@echo "📊 Running test coverage..."
	@coverage run -m pytest && coverage report -m
	@echo "✅ Coverage report generated."

.PHONY: docker-up
docker-up:
	@echo "🐳 Starting Docker containers..."
	@docker compose -f $(DOCKER_COMPOSE_FILE) up -d
	@sleep 2
	@$(BROWSER) http://0.0.0.0:8002/docs
	@echo "✅ Docker containers are up."

.PHONY: docker-build
docker-build:
	@echo "🔨 Building and starting Docker containers..."
	@docker compose -f $(DOCKER_COMPOSE_FILE) up -d --build
	@sleep 2
	@$(BROWSER) http://0.0.0.0:8002/docs
	@echo "✅ Docker containers built and started."

.PHONY: docker-stop
docker-stop:
	@echo "🛑 Stopping and removing Docker containers..."
	@docker compose -f $(DOCKER_COMPOSE_FILE) down
	@echo "✅ Docker containers stopped and removed."


.PHONY: api
api:
	@echo "🚀 Starting API..."
	@forecast-api
# @sleep 2
# @echo "🌍 Opening API in browser..."
# @$(BROWSER) http://127.0.0.1:8000/docs

.PHONY: ui
ui:
	@echo "📊 Starting Streamlit UI..."
# save the PID of the Streamlit UI process
	@forecast-ui & echo $$! > .ui_pid
	@sleep 2

.PHONY: stop-ui
stop-ui:
# if the pid exists, kill the process and remove the file
	@if [ -f .ui_pid ]; then \
		echo "🛑 Stopping Streamlit UI..."; \
		kill `cat .ui_pid` && rm .ui_pid; \
		echo "✅ Streamlit UI stopped."; \
	else \
		echo "⚠️  Streamlit UI is not running."; \
	fi

.PHONY: clean
clean:
	@echo "🧹 Cleaning up..."
	@if [ -d ".venv" ]; then \
		echo "❌ Deactivating and removing virtual environment..."; \
		source .venv/bin/activate && deactivate && rm -rf .venv; \
	fi
	@if [ -f ".ui_pid" ]; then \
		rm .ui_pid; \
	fi
	rm -rf .coverage *.log .pytest_cache
	@find forecasting -name "__pycache__" -type d -exec rm -rf {} +
	@echo "✅ Clean up complete."
