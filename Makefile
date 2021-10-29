.PHONY: install-base
# Install base setup tools
install-base:
	pip install -U pip setuptools poetry

.PHONY: install
# Install the dependencies needed for a production installation
install:: install-base
	poetry install --no-dev

.PHONY: install-ci
# Install the tools necessary for CI
install-ci:: install-base

install-ci::
	poetry install --extras test --extras dev-tools

.PHONY: install-dev
# install development dependencies
install-dev:: install-base
	poetry install --extras test --extras dev-tools

install-dev::
	pip install pre-commit
	pre-commit install

.PHONY: clean
## clean temporary files
clean:: clean-build clean-pyc

.PHONY: cleanall
## clean temporary files and caches
cleanall: clean clean-mypy clean-precommit

.PHONY: clean-build

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	rm -fr *.spec

.PHONY: clean-pyc
clean-pyc:
	find . -name '*~' -exec rm -f {} +
	find . -name '*.log*' -delete
	find . -name '*_cache' -exec rm -rf {} +
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

.PHONY: clean-mypy
# delete the mypy cache
clean-mypy:
	rm -rf .mypy_cache

.PHONY: clean-precommit
# clean up the pre-commit caches
clean-precommit:
	poetry run pre-commit clean

.PHONY: pre-commit
# run the pre-commit checks
pre-commit:
	poetry run pre-commit run --all-files

.PHONY: lint
# run flake8 against src
lint:
	poetry run flake8 src

.PHONY: isort
# run isort against src
isort:
	poetry run isort src

.PHONY: black
# run black against src
black:
	poetry run black src

.PHONY: mypy
# run mypy against src
mypy:
	poetry run mypy src
