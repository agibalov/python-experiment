from typing import Optional

import connexion
import flask.testing
import pytest


def get_people(
        name: Optional[str] = None,
        page: Optional[int] = None):

    return {
        'name': name,
        'page': page
    }


app = connexion.FlaskApp(__name__)
app.add_api('nullable_query_params_api.yaml')

if __name__ == '__main__':
    app.run(port=8080)


@pytest.fixture
def client() -> flask.testing.FlaskClient:
    yield app.app.test_client()


def test_it_applies_defaults(client: flask.testing.FlaskClient):
    response = client.get('/people')
    assert response.status_code == 200
    assert response.get_json() == {
        'name': None,
        'page': None
    }


def test_it_handles_non_defaults(client: flask.testing.FlaskClient):
    response = client.get('/people', query_string={'name': 'Ste', 'page': 1})
    assert response.status_code == 200
    assert response.get_json() == {
        'name': 'Ste',
        'page': 1
    }
