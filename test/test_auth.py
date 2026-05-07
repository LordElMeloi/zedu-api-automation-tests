import requests
from jsonschema import validate
from utils.auth import register_user, login_user, extract_access_token, get_base_url


LOGIN_SUCCESS_SCHEMA = {
    "type": "object",
    "required": ["status", "status_code", "message", "data"],
    "properties": {
        "status": {"type": "string"},
        "status_code": {"type": "integer"},
        "message": {"type": "string"},
        "data": {
            "type": "object",
            "required": ["user", "access_token", "access_token_expires_in", "notification_token"],
            "properties": {
                "user": {"type": "object"},
                "access_token": {"type": "string"},
                "access_token_expires_in": {"type": "string"},
                "notification_token": {"type": "string"},
            },
        },
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

SUCCESS_SCHEMA = {
    "type": "object",
    "required": ["status", "status_code", "message"],
    "properties": {
        "status": {"type": "string"},
        "status_code": {"type": "integer"},
        "message": {"type": "string"},
    },
}


def test_register_with_valid_data_to_returns_201():
    response, email, password = register_user()

    data = response.json()

    assert response.status_code == 201
    assert data["status"] == "success"
    assert data["status_code"] == 201
    assert "message" in data
    assert isinstance(data["message"], str)


def test_successful_login_returns_200_and_access_token():
    register_response, email, password = register_user()
    assert register_response.status_code == 201

    login_response = login_user(email, password)
    data = login_response.json()

    assert login_response.status_code == 200
    validate(instance=data, schema=LOGIN_SUCCESS_SCHEMA)

    assert data["status"] == "success"
    assert data["status_code"] == 200
    assert "data" in data
    assert "access_token" in data["data"]
    assert isinstance(data["data"]["access_token"], str)
    assert len(data["data"]["access_token"]) > 0


def test_login_with_invalid_password_returns_an_error():
    register_response, email, password = register_user()
    assert register_response.status_code == 201

    login_response = login_user(email, "WrongPassword123")
    data = login_response.json()

    assert login_response.status_code in [400, 401, 422]
    validate(instance=data, schema=ERROR_SCHEMA)

    assert "message" in data
    assert isinstance(data["message"], str)


def test_login_with_missing_password_returns_error():
    register_response, email, password = register_user()
    assert register_response.status_code == 201

    from utils.auth import get_base_url
    base_url = get_base_url()

    payload = {
        "email": email
    }

    response = requests.post(f"{base_url}/auth/login", json=payload, timeout=30)
    data = response.json()

    assert response.status_code in [400, 401, 422]
    validate(instance=data, schema=ERROR_SCHEMA)

    assert "message" in data
    assert isinstance(data["message"], str)

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

