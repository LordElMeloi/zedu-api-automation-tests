import requests
from jsonschema import validate
from utils.auth import get_base_url


SUCCESS_SCHEMA = {
    "type": "object",
    "required": ["status", "status_code", "message"],
    "properties": {
        "status": {"type": "string"},
        "status_code": {"type": "integer"},
        "message": {"type": "string"},
    },
}

ERROR_SCHEMA = {
    "type": "object",
    "required": ["status", "status_code", "message"],
    "properties": {
        "status": {"type": "string"},
        "status_code": {"type": "integer"},
        "message": {"type": "string"},
    },
}


def test_logout_is_successful(auth_headers):
    response = requests.post(
        f"{get_base_url()}/auth/logout",
        headers=auth_headers,
        timeout=30,
    )

    data = response.json()

    assert response.status_code == 200
    validate(instance=data, schema=SUCCESS_SCHEMA)
    assert data["status"] == "success"
    assert data["status_code"] == 200


def test_logout_without_token_returns_401_unauthorized():
    response = requests.post(
        f"{get_base_url()}/auth/logout",
        headers={"X-Platform": "web"},
        timeout=30,
    )

    data = response.json()

    assert response.status_code in [400, 401]
    validate(instance=data, schema=ERROR_SCHEMA)


def test_logout_with_invalid_token_returns_401_unauthorized():
    headers = {
        "Authorization": "Bearer invalidtoken123",
        "X-Platform": "web",
    }

    response = requests.post(
        f"{get_base_url()}/auth/logout",
        headers=headers,
        timeout=30,
    )

    data = response.json()

    assert response.status_code in [400, 401]
    validate(instance=data, schema=ERROR_SCHEMA)


def test_logout_with_missing_platform_header():
    headers = {
        "Authorization": "Bearer invalidtoken123"
    }

    response = requests.post(
        f"{get_base_url()}/auth/logout",
        headers=headers,
        timeout=30,
    )

    data = response.json()

    assert response.status_code in [200, 400, 401, 422]

    assert "status" in data
    assert "message" in data
