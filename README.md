# Zedu API Automation Tests

![CI](https://github.com/LordElMeloi/zedu-api-automation-tests/actions/workflows/ci.yml/badge.svg)

## Overview

This project contains automated API tests for the Zedu platform using Python, Pytest, and Requests.

The suite covers authentication and user-flow endpoints from the Zedu Swagger documentation, with tests for:
- positive scenarios
- negative scenarios
- boundary cases
- edge cases
- token-based authorization

The goal of the project is to validate API behavior in a clean, maintainable, and repeatable way.

## Tech Stack

- Python 3.13.x
- Pytest
- Requests
- python-dotenv
- jsonschema

## Prerequisites

Before running the project, ensure the following are installed:

- Python 3.13.x
- pip
- git

## Project Structure

```text
zedu-api-automation-tests/
├── tests/
│   ├── test_auth.py
│   ├── test_users.py
│   ├── test_validation.py
│   └── test_edge_cases.py
├── utils/
│   ├── auth.py
│   └── users.py
├── conftest.py
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── .github/
    └── workflows/
        └── ci.yml
```
## Test File Coverage

## test/test_auth.py

Covers authentication-related flows such as registration, login, logout, token extraction, and authentication failure handling.

## test/test_users.py

Covers user-flow GET endpoints such as:

/users/me
/users/{userId}
/users/{user_id}/status
/users/{userId}/login-audit
/users/organisations
tests/test_validation.py

Covers missing fields, invalid formats, invalid data types, and boundary value checks.

## tests/test_edge_cases.py

Covers unusual but realistic inputs such as whitespace, casing differences, long values, and optional-field variations.

Design Decisions
Why helper functions are used

Reusable API request logic is placed in utils/ so that request handling is centralized and test files remain readable.

Why fixtures are used

Shared Pytest fixtures in conftest.py handle setup logic such as creating a fresh user, logging in, extracting the token, and building auth headers. This keeps tests independent and avoids duplicated setup code.

Why dynamic data is used

Unique data is generated where needed so the suite remains idempotent and can be run multiple times without failing because of reused emails or shared state.

Why tests are grouped by behavior

Test files are organized by feature area so the suite is easier to understand, maintain, and extend.

Why schema validation is included

Schema checks confirm that responses are not only successful, but also structurally correct and consistent with backend expectations.

Virtual Environment Setup

Using a virtual environment is recommended so dependencies stay isolated from your system Python.

## Linux / macOS
```bash
python -m venv .venv
source .venv/bin/activate
```
## Windows
```bash
python -m venv .venv
.\.venv\Scripts\activate
```
## Install Dependencies

Install all required packages with:

``` bash
pip install -r requirements.txt
Environment Variables
```

Create a .env file in the project root with the following values:

```
BASE_URL=https://api.zedu.chat/api/v1
EMAIL=your_email_here
PASSWORD=your_password_here
```
Do not commit the .env file to GitHub.

A template is provided in .env.example for convenience.

Running the Test Suite Locally

Run the full suite with:
```bash
pytest -v
```
To generate a JUnit XML report locally:
```bash
pytest --junitxml=reports/junit.xml
```
## CI Pipeline

This repository is configured to run automatically using GitHub Actions.

The pipeline:

triggers on push
triggers on pull request
installs dependencies automatically
runs the full Pytest suite
generates a JUnit XML test report
uploads the report as a build artifact
fails the pipeline if any test fails
## How to Run from a Clean Clone
``` bash
git clone https://github.com/LordElMeloi/zedu-api-automation-tests.git
cd zedu-api-automation-tests
```
```
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```
cp .env.example .env
# Edit .env and add your actual values

pytest -v
Notes
Authentication tokens are handled dynamically.
No hardcoded tokens are used in the codebase.
No hardcoded base URL is used in test files.
Tests are designed to be repeatable and independent.
The repository should remain public for submission.
CI Badge

If the badge does not render immediately, wait until the first successful workflow run on GitHub Actions.

Troubleshooting
Missing environment variables

If pytest fails because of missing values, confirm that .env exists in the project root and contains the correct values.

Dependency errors

If imports fail, re-run:
```bash
pip install -r requirements.txt
```
Token or authorization issues

If user-flow tests fail, confirm that the login endpoint returns an access token and that your fixtures are extracting it correctly.

Unexpected API response structure

If a test fails because of a schema or field mismatch, check the actual response body and align the assertion with the live API behavior.

## What This Project Demonstrates

This project demonstrates:

structured API automation
reusable test helpers
dynamic authentication handling
clean separation of setup and assertions
backend validation coverage
production-minded test organization
CI-ready automation
