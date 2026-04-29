import pytest
from jsonschema import validate
from utils.auth import register_user, register_raw


ERROR_SCHEMA = {
    "type": "object",
    "required": ["status", "status_code", "message"],
    "properties": {
        "status": {"type": "string"},
        "status_code": {"type": "integer"},
        "message": {"type": "string"},
    },
}

SUCCESS_SCHEMA = {
    "type": "object",
    "required": ["status", "status_code", "message"],
    "properties": {
        "status": {"type": "string"},
        "status_code": {"type": "integer"},
        "message": {"type": "string"},
    },
}


@pytest.mark.parametrize(
    "payload, expected_status",
    [
        pytest.param({"password": "TestPassword123"}, 422, id="missing_email_returns_422"),
        pytest.param({"email": "test@example.com"}, 422, id="missing_password_returns_422"),
        pytest.param({"email": "invalidemail", "password": "TestPassword123"}, 400, id="invalid_email_returns_400"),
        pytest.param({}, 422, id="empty_payload_returns_422"),
        pytest.param({"email": "test@example.com", "password": "123"}, 400, id="short_password_returns_400"),
        pytest.param({"email": "a" * 250 + "@example.com", "password": "TestPassword123"}, 400, id="very_long_email_returns_400"),
    ],
)

def test_register_with_invalid_inputs_returns_expected_errors(payload, expected_status):
    response = register_raw(payload)
    data = response.json()

    assert response.status_code == expected_status
    validate(instance=data, schema=ERROR_SCHEMA)
    assert "message" in data
    assert isinstance(data["message"], str)



def test_register_minimum_password_length_returns201():
    response = register_raw({
        "email": "minpass@example.com",
        "password": "TestPass",   # 8 chars
        "first_name": "Test",
        "last_name": "User"
    })
    data = response.json()

    assert response.status_code == 200
    validate(instance=data, schema=SUCCESS_SCHEMA)


def test_register_maximum_password_length_returns201():
    response = register_raw({
        "email": "maxpass@example.com",
        "password": "TestPassword1234",   # 16 chars
        "first_name": "Test",
        "last_name": "User"
    })
    data = response.json()

    assert response.status_code == 200
    validate(instance=data, schema=SUCCESS_SCHEMA)
