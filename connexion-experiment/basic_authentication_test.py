import pytest
import connexion
import flask.testing
import base64


def get_secret(user):
    return {
        'message': 'hi {}!'.format(user)
    }


def basic_auth(username, password, required_scopes=None):
    if username == 'user1' and password == 'qwerty':
        return {'sub': username}
    return None


app = connexion.FlaskApp(__name__)
app.add_api('basic_authentication_api.yaml')
if __name__ == '__main__':
    app.run(port=8080)


@pytest.fixture
def client()-> flask.testing.FlaskClient:
    yield app.app.test_client()


def test_get_secret_responds_with_200_when_username_and_password_are_valid(client: flask.testing.FlaskClient):
    response = client.get('/secret', headers={
        'Authorization': make_authorization_header('user1', 'qwerty')
    })
    assert response.status_code == 200
    assert response.get_json() == {
        'message': 'hi user1!'
    }


def test_get_secret_responds_with_401_when_username_and_password_are_not_valid(client: flask.testing.FlaskClient):
    response = client.get('/secret', headers={
        'Authorization': make_authorization_header('hacker', '123456')
    })
    assert response.status_code == 401
    assert response.get_json() == {
        'detail': 'Provided authorization is not valid',
        'status': 401,
        'title': 'Unauthorized',
        'type': 'about:blank'
    }


def make_authorization_header(username: str, password: str) -> str:
    username_password_string = '{}:{}'.format(username, password)
    return 'Basic {}'.format(base64.standard_b64encode(username_password_string.encode()).decode())
