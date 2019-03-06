import pytest
from main import connexion_app
import flask.testing


@pytest.fixture
def client()-> flask.testing.FlaskClient:
    flask_app = connexion_app.app
    yield flask_app.test_client()


def test_get_hello_should_say_hello_world(client: flask.testing.FlaskClient):
    response = client.get('/hello')
    assert response.status_code == 200
    assert response.get_json() == {
        'message': 'hello world!'
    }
