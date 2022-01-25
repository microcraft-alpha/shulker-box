.PHONY: lint
## Run pre-commit checks
lint:
	poetry run pre-commit run --all-files

.PHONY: test
## Run pytest
test:
	poetry run pytest
