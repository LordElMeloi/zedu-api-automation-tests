# Zedu API Automation Tests

![CI](https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPO_NAME>/actions/workflows/ci.yml/badge.svg)

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
