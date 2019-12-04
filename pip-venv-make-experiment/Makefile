SHELL := /bin/bash

clean-devenv:
	rm -rf ./venv

.ONESHELL:
devenv:
	python -m venv ./venv
	source ./venv/bin/activate
	pip install --upgrade pip
	pip install -r requirements/dev.pip

run: devenv
	source ./venv/bin/activate
	python experiment/__init__.py

docker-run:
	docker-compose up --build

.ONESHELL:
test: devenv
	source ./venv/bin/activate
	flake8 &&	\
	mypy experiment --strict && \
	pytest
