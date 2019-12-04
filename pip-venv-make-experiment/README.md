# pip-venv-make-experiment

Goal: learn how people do it without Pipenv.

* `make devenv` to create the virtual environment (at `./venv`) and install all the dev dependencies. You can then `source ./venv/bin/activate` to activate it (and then `deactivate` to deactivate).
* `make clean-devenv` to delete the virtual environment.
* `make test` to run flake8, mypy and pytest.
* `make run` to run the app using Flask dev server. The app will be available at http://localhost:5000/
* `make docker-run` to run the app using Docker Compose (uses Gunicorn). The app will be available at http://localhost:8080/
