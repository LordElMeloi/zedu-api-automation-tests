import pytest
from utils.auth import register_user, login_user, extract_access_token


@pytest.fixture(scope="function")
def fresh_user():
    response, email, password = register_user()
    assert response.status_code == 201, f"User registration failed: {response.text}"
    return email, password


@pytest.fixture(scope="function")
def logged_in_user(fresh_user):
    email, password = fresh_user
    login_response = login_user(email, password)
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"

    token = extract_access_token(login_response)
    return {
        "email": email,
        "password": password,
        "login_response": login_response,
        "token": token,
    }


@pytest.fixture(scope="function")
def auth_headers(logged_in_user):
    return {
        "Authorization": f"Bearer {logged_in_user['token']}",
        "X-Platform": "web",
    }
