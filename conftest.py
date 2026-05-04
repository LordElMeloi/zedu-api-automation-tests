import pytest
from utils.auth import register_user, login_user, extract_access_token
from utils.users import get_current_user


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

    login_data = login_response.json()
    user_block = login_data.get("data", {}).get("user", {})

    user_id = user_block.get("id") or user_block.get("user_id")
    assert user_id, f"User ID not found in login response: {login_response.text}"

    token = extract_access_token(login_response)

    return {
        "email": email,
        "password": password,
        "login_response": login_response,
        "token": token,
        "user_id": user_id,
    }



@pytest.fixture(scope="function")
def auth_headers(logged_in_user):
    return {
        "Authorization": f"Bearer {logged_in_user['token']}",
    }


@pytest.fixture(scope="function")
def current_user(auth_headers, logged_in_user):
    response = get_current_user(auth_headers)
    assert response.status_code == 200, f"Fetching current user failed: {response.text}"

    data = response.json()
    user_data = data.get("data", {}).get("user", {})

    assert user_data, f"User object not found in /users/me response: {response.text}"

    return {
        "response": response,
        "data": data,
        "user_id": logged_in_user["user_id"],
        "user_data": user_data,
    }
