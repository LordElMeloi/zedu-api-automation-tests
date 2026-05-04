import requests
from jsonschema import validate
from utils.users import (
    get_base_url,
    get_current_user,
    get_user_by_id,
    get_user_status,
    get_login_audit,
    get_user_organisations,
)


SUCCESS_SCHEMA = {
    "type": "object",
    "required": ["status"],
    "properties": {
        "status": {"type": "string"},
        "message": {"type": "string"},
        "data": {},
    },
    "additionalProperties": True,
}

ERROR_SCHEMA = {
    "type": "object",
    "required": ["status"],
    "properties": {
        "status": {"type": "string"},
        "message": {"type": "string"},
        "error": {"type": "string"},
    },
    "additionalProperties": True,
}


def test_get_current_user_with_valid_token_returns_200_and_user_object(auth_headers):
    response = get_current_user(auth_headers)
    data = response.json()

    assert response.status_code == 200
    validate(instance=data, schema=SUCCESS_SCHEMA)

    assert data["status"] == "success"
    assert "data" in data
    assert "user" in data["data"]
    assert isinstance(data["data"]["user"], dict)
    assert "email" in data["data"]["user"]


def test_get_current_user_without_token_returns_unauthorized():
    response = requests.get(f"{get_base_url()}/users/me", timeout=30)
    data = response.json()

    assert response.status_code in [401, 403]
    validate(instance=data, schema=ERROR_SCHEMA)
    assert "status" in data


def test_get_user_by_valid_id_returns_200(current_user, auth_headers):
    user_id = current_user["user_id"]
    response = get_user_by_id(user_id, auth_headers)
    data = response.json()

    assert response.status_code == 200
    validate(instance=data, schema=SUCCESS_SCHEMA)

    assert data["status"] == "success"
    assert "data" in data


def test_get_user_by_invalid_id_format_returns_error(auth_headers):
    response = get_user_by_id("invalid-id-format", auth_headers)
    data = response.json()

    assert response.status_code in [400, 404, 422]
    validate(instance=data, schema=ERROR_SCHEMA)


def test_get_user_status_with_valid_id_returns_200(current_user, auth_headers):
    user_id = current_user["user_id"]
    response = get_user_status(user_id, auth_headers)
    data = response.json()

    assert response.status_code == 200
    validate(instance=data, schema=SUCCESS_SCHEMA)

    assert data["status"] == "success"


def test_get_login_audit_with_valid_id_returns_200(current_user, auth_headers):
    user_id = current_user["user_id"]
    response = get_login_audit(user_id, auth_headers)
    data = response.json()

    assert response.status_code == 200
    validate(instance=data, schema=SUCCESS_SCHEMA)

    assert data["status"] == "success"
    assert "data" in data


def test_get_user_organisations_returns_200(auth_headers):
    response = get_user_organisations(auth_headers)
    data = response.json()

    assert response.status_code == 200
    validate(instance=data, schema=SUCCESS_SCHEMA)

    assert data["status"] == "success"
    assert "data" in data
