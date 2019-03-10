from main import app
from pytest import fixture


@fixture
def client():
    yield app.test_client()


def test_get_hello_plaintext(client):
    response = client.get('/hello/plaintext')
    assert response.status_code == 200
    assert b'hi there' in response.data


def test_get_hello_json(client):
    response = client.get('/hello/json')
    assert response.status_code == 200
    assert response.get_json() == {
        'message': 'hi there!!!1'
    }
