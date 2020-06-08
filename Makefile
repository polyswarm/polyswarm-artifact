.PHONY: help clean lint format test
.DEFAULT_GOAL := help
SRCDIR := src/polyswarmartifact/

define PRINT_HELP_PYSCRIPT
import re, sys
for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
	  target, help = match.groups()
	  print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: ## remove build artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	rm -fr .pytest_cache/
	find . \( -path ./env -o -path ./venv -o -path ./.env -o -path ./.venv \) -prune -o -name '*.egg-info' -exec rm -fr {} +
	find . \( -path ./env -o -path ./venv -o -path ./.env -o -path ./.venv \) -prune -o -name '*.egg' -exec rm -f {} +

lint: ## check style
	-mypy
	-flake8 $(SRCDIR) tests
	-yapf -p -r -d $(SRCDIR)
	-isort --recursive --diff $(SRCDIR)

format:  ## format code in Polyswarm style
	yapf -p -r -i $(SRCDIR) tests
	isort --recursive $(SRCDIR) tests

test: ## run tests
	py.test
