DIR := .

.PHONY: init lint fix format check test all app

init: 
	curl -LsSf https://astral.sh/uv/install.sh | sh
	uv sync

lint:
	uv run ruff check ${DIR}
	uv run sqlfluff lint ${DIR}

fix:
	uv run ruff check --fix ${DIR}
	uv run sqlfluff fix ${DIR}

format:
	uv run ruff format ${DIR}


check: fix lint format

test:
	uv run pytest -o log_cli=true -o log_cli_level=DEBUG

all: check test

app:
	uv run src/app.py