import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_base_url():
    base_url = os.getenv("BASE_URL")
    if not base_url:
        raise ValueError("BASE_URL is missing in .env")
    return base_url


def get_current_user(auth_headers):
    base_url = get_base_url()
    return requests.get(f"{base_url}/users/me", headers=auth_headers, timeout=30)


def get_user_by_id(user_id, auth_headers):
    base_url = get_base_url()
    return requests.get(f"{base_url}/users/{user_id}", headers=auth_headers, timeout=30)


def get_user_status(user_id, auth_headers):
    base_url = get_base_url()
    return requests.get(f"{base_url}/users/{user_id}/status", headers=auth_headers, timeout=30)


def get_login_audit(user_id, auth_headers):
    base_url = get_base_url()
    return requests.get(f"{base_url}/users/{user_id}/login-audit", headers=auth_headers, timeout=30)


def get_user_organisations(auth_headers):
    base_url = get_base_url()
    return requests.get(f"{base_url}/users/organisations", headers=auth_headers, timeout=30)
