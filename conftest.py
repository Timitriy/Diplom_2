import pytest
import requests
import random

BASE_URL = "https://stellarburgers.nomoreparties.site/api"


@pytest.fixture
def registered_user():
    email = f"test_{random.randint(1000, 9999)}@example.com"
    password = "password123"
    name = "Test User"

    payload = {
        "email": email,
        "password": password,
        "name": name
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=payload)

    if response.status_code == 403:
        pytest.skip("User already exists")

    return {
        "email": email,
        "password": password,
        "name": name
    }


@pytest.fixture
def authorized_user(registered_user):
    payload = {
        "email": registered_user["email"],
        "password": registered_user["password"]
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    assert response.status_code == 200

    return {
        "email": registered_user["email"],
        "token": response.json()["accessToken"]
    }


@pytest.fixture
def valid_ingredients():
    response = requests.get(f"{BASE_URL}/ingredients")
    assert response.status_code == 200
    ingredients = response.json()["data"]
    return [ingredients[0]["_id"], ingredients[1]["_id"]]