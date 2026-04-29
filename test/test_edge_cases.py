import uuid
import pytest
from jsonschema import validate
from utils.auth import register_raw


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


def build_base_payload():
    suffix = uuid.uuid4().hex[:8]
    return {
        "username": f"edge_{suffix}",
        "email": f"edge_{suffix}@example.com",
        "password": "TestPassword123",
        "first_name": "Test",
        "last_name": "User",
    }


@pytest.mark.parametrize(
    "description, overrides, allowed_statuses",
    [
        (
            "first_name with leading and trailing spaces",
            {"first_name": "  David  "},
            [201, 400, 422],
        ),
        (
            "last_name with leading and trailing spaces",
            {"last_name": "  Umoh  "},
            [201, 400, 422],
        ),
        (
            "email in uppercase",
            {"email": f"EDGE_{uuid.uuid4().hex[:8]}@EXAMPLE.COM"},
            [201, 400, 422],
        ),
        (
            "email with plus alias",
            {"email": f"edge+{uuid.uuid4().hex[:6]}@example.com"},
            [201, 400, 422],
        ),
        (
            "very long first_name",
            {"first_name": "A" * 120},
            [201, 400, 422],
        ),
        (
            "very long last_name",
            {"last_name": "B" * 120},
            [201, 400, 422],
        ),
        (
            "password with surrounding spaces",
            {"password": "  TestPassword123  "},
            [201, 400, 422],
        ),
        (
            "username with surrounding spaces",
            {"username": "  edge_user  "},
            [201, 400, 422],
        ),
        (
            "phone_number provided as a numeric string",
            {"phone_number": "08012345678"},
            [201, 400, 422],
        ),
    ],
)
def test_register_edge_cases(description, overrides, allowed_statuses):
    payload = build_base_payload()
    payload.update(overrides)

    response = register_raw(payload)
    data = response.json()

    assert response.status_code in allowed_statuses

    if response.status_code in [200, 201]:
        validate(instance=data, schema=SUCCESS_SCHEMA)
        assert data["status"] == "success"
        assert isinstance(data["message"], str)
    else:
        validate(instance=data, schema=ERROR_SCHEMA)
        assert "message" in data
        assert isinstance(data["message"], str)
