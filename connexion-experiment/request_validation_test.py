import pytest
import connexion
import flask.testing


def add_numbers(a, b):
    return {
        'result': a + b
    }


def add_numbers_json(body):
    return {
        'result': body['a'] + body['b']
    }


def get_user(id: int):
    return {
        'id': id,
        'name': 'User #{}'.format(id)
    }


app = connexion.FlaskApp(__name__)
app.add_api('request_validation_api.yaml')
if __name__ == '__main__':
    app.run(port=8080)


@pytest.fixture
def client()-> flask.testing.FlaskClient:
    yield app.app.test_client()


def test_add_numbers_responds_with_200_when_parameters_are_numbers(client: flask.testing.FlaskClient):
    response = client.get('/add_numbers', query_string={'a': 2, 'b': 3})
    assert response.status_code == 200
    assert response.get_json() == {
        'result': 5
    }


def test_add_numbers_responds_with_400_when_parameters_are_strings(client: flask.testing.FlaskClient):
    response = client.get('/add_numbers', query_string={'a': 'hello', 'b': 'world'})
    assert response.status_code == 400
    # NOTE: only mentions 'a'
    assert response.get_json() == {
        'detail': "Wrong type, expected 'number' for query parameter 'a'",
        'status': 400,
        'title': 'Bad Request',
        'type': 'about:blank'
    }


def test_add_numbers_json_responds_with_200_when_parameters_are_numbers(client: flask.testing.FlaskClient):
    response = client.post('/add_numbers_json', json={
        'a': 2,
        'b': 3
    })
    assert response.status_code == 200
    assert response.get_json() == {
        'result': 5
    }


def test_add_numbers_json_responds_with_400_when_parameters_are_strings(client: flask.testing.FlaskClient):
    response = client.post('/add_numbers_json', json={
        'a': 'hello',
        'b': 'world'
    })
    assert response.status_code == 400
    # NOTE: does not even explain if it's 'a' or 'b'
    assert response.get_json() == {
        'detail': "'hello' is not of type 'number'",
        'status': 400,
        'title': 'Bad Request',
        'type': 'about:blank'
    }


def test_get_user_responds_with_200_when_user_id_is_an_integer(client: flask.testing.FlaskClient):
    response = client.get('/users/123')
    assert response.status_code == 200
    assert response.get_json() == {
        'id': 123,
        'name': 'User #123'
    }


def test_get_user_responds_with_404_when_user_id_is_a_string(client: flask.testing.FlaskClient):
    response = client.get('/users/hello')
    assert response.status_code == 404
