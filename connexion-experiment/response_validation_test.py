import pytest
import connexion
import flask.testing


def get_message(return_valid_response: bool):
    if return_valid_response:
        return {
            'message': 'hi there'
        }

    return {
        'xxx': 123
    }


app = connexion.FlaskApp(__name__)
app.add_api('response_validation_api.yaml', validate_responses=True)
if __name__ == '__main__':
    app.run(port=8080)


@pytest.fixture
def client()-> flask.testing.FlaskClient:
    yield app.app.test_client()


def test_get_message_responds_with_200_when_response_is_valid(client: flask.testing.FlaskClient):
    response = client.get('/message', query_string={'return_valid_response': True})
    assert response.status_code == 200
    assert response.get_json() == {
        'message': 'hi there'
    }


def test_get_message_responds_with_500_when_response_does_not_match_the_api_spec(client: flask.testing.FlaskClient):
    response = client.get('/message', query_string={'return_valid_response': False})
    assert response.status_code == 500
    assert response.get_json()['title'] == 'Response body does not conform to specification'
