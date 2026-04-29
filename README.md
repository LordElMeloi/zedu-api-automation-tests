# Zedu API Automation Tests

## Overview
Automated API tests for authentication endpoints using Pytest.

## Setup
1. Clone repo
2. Create .env file:
   BASE_URL=https://api.zedu.chat/api/v1
   EMAIL=your_email
   PASSWORD=your_password

3. Install dependencies:
   pip install -r requirements.txt

## Run Tests
pytest -v

## Structure
- tests/: test files
- utils/: reusable functions
- conftest.py: shared fixtures
