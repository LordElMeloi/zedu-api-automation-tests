import os
import uuid
import requests
from dotenv import load_dotenv

load_dotenv()


def get_base_url():
    base_url = os.getenv("BASE_URL")
    if not base_url:
        raise ValueError("BASE_URL is missing in .env")
    return base_url


def generate_unique_email():
    return f"test_{uuid.uuid4().hex[:8]}@example.com"


def register_user(
    email=None,
    password=None,
    first_name="Test",
    last_name="User",
    username=None,
    phone_number=None,
):
    base_url = get_base_url()

    payload = {
        "email": email or generate_unique_email(),
        "password": password or "TestPassword123",
        "first_name": first_name,
        "last_name": last_name,
    }

    if username is not None:
        payload["username"] = username

    if phone_number is not None:
        payload["phone_number"] = phone_number

    response = requests.post(f"{base_url}/auth/register", json=payload, timeout=30)
    return response, payload["email"], payload["password"]


def login_user(email, password):
    base_url = get_base_url()

    payload = {
        "email": email,
        "password": password,
    }

    response = requests.post(f"{base_url}/auth/login", json=payload, timeout=30)
    return response


def extract_access_token(login_response):
    data = login_response.json()

    token = None
    if isinstance(data.get("data"), dict):
        token = data["data"].get("access_token")
    if not token:
        token = data.get("access_token")

    if not token:
        raise ValueError("Access token not found in login response")

    return token


def logout_user(access_token):
    base_url = get_base_url()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Platform": "web",
    }

    response = requests.post(f"{base_url}/auth/logout", headers=headers, timeout=30)
    return response

def register_raw(payload):
    base_url = get_base_url()
    return requests.post(f"{base_url}/auth/register", json=payload, timeout=30)


def login_raw(payload):
    base_url = get_base_url()
    return requests.post(f"{base_url}/auth/login", json=payload, timeout=30)
