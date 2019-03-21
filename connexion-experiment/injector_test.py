import connexion
import flask.testing
import flask_injector
import pytest
from injector import Binder, Injector

from injector_test_handler import MessageGenerator


def configure_for_prod(binder: Binder):
    binder.bind(MessageGenerator, to=MessageGenerator(message='hi there prod!'))


def configure_for_test(binder: Binder):
    binder.bind(MessageGenerator, to=MessageGenerator(message='hi there test!'))


app = connexion.FlaskApp(__name__)
app.add_api('injector_api.yaml')

if __name__ == '__main__':
    modules = [configure_for_prod]
else:
    modules = [configure_for_test]

injector = Injector(modules)
flask_injector.FlaskInjector(app=app.app, injector=injector)

if __name__ == '__main__':
    app.run(port=8080)


@pytest.fixture
def client() -> flask.testing.FlaskClient:
    yield app.app.test_client()


def test_get_message(client: flask.testing.FlaskClient):
    response = client.get('/message')
    assert response.status_code == 200
    assert response.get_json() == {
        'message': 'hi there test!'
    }
