.PHONY: test dev lint type qa

dev:
	pip install -e ".[dev]"
	python3 validator/post-install.py

lint:
	ruff check .

test:
	pytest -v tests

type:
	pyright validator

qa:
	make lint
	make type
	make test
	