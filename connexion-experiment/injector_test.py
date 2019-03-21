import connexion
import flask.testing
import flask_injector
import pytest
from injector import Binder, Injector, CallableProvider

from injector_test_handler import MessageGenerator, Count

count = 0


def make_configuration(text: str):
    def configure(binder: Binder):
        def get_count():
            global count
            count = count + 1
            return count
        binder.bind(Count, to=CallableProvider(get_count), scope=flask_injector.request)
        binder.bind(MessageGenerator, to=MessageGenerator(message='hi there {}!'.format(text)))
    return configure


app = connexion.FlaskApp(__name__)
app.add_api('injector_api.yaml')

if __name__ == '__main__':
    modules = [make_configuration('prod')]
else:
    modules = [make_configuration('test')]

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
        'message': 'hi there test!',
        'count': 1
    }
