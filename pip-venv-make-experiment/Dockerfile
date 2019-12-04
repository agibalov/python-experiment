FROM python:3.7.1

COPY . /app
WORKDIR /app

SHELL ["/bin/bash", "-c"]

RUN python -m venv ./venv && \
  source ./venv/bin/activate && \
  pip install --upgrade pip && \
  pip install -r requirements/run.pip

ENTRYPOINT ["./docker-entrypoint.sh"]
