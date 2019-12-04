from typing import Any

import pytest

from experiment import app


@pytest.fixture  # type: ignore
def client() -> Any:
    with app.test_client() as client:
        yield client


def test_dummy(client: Any) -> None:
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {
        'message': 'hello world'
    }
