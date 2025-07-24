import pytest
import requests
import random
from http import HTTPStatus

# Базовый URL и эндпоинты
BASE_URL = "https://stellarburgers.nomoreparties.site/api"
ENDPOINTS = {
    "REGISTER": "/auth/register",
    "LOGIN": "/auth/login",
    "USER": "/auth/user",
    "INGREDIENTS": "/ingredients",
    "ORDERS": "/orders"
}

# Сообщения ошибок / статусы
ERR_NO_INGREDIENTS = "Ingredient ids must be provided"
ERR_USER_EXISTS = "User already exists"
ERR_REQUIRED_FIELDS = "Email, password and name are required fields"
ERR_UNAUTHORIZED = "You should be authorised"
ERR_WRONG_CREDENTIALS = "email or password are incorrect"


@pytest.fixture
def registered_user():
    """Регистрирует нового пользователя и возвращает его данные."""
    email = f"test_{random.randint(1000, 9999)}@example.com"
    password = "password123"
    name = "Test User"

    payload = {"email": email, "password": password, "name": name}
    response = requests.post(f"{BASE_URL}{ENDPOINTS['REGISTER']}", json=payload)

    if response.status_code == HTTPStatus.FORBIDDEN:
        pytest.skip("User already exists, skipping registration fixture")

    assert response.status_code == HTTPStatus.OK
    return {"email": email, "password": password, "name": name}


@pytest.fixture
def authorized_user(registered_user):
    """Логинится зарегистрированным пользователем и возвращает токен."""
    payload = {"email": registered_user["email"], "password": registered_user["password"]}
    response = requests.post(f"{BASE_URL}{ENDPOINTS['LOGIN']}", json=payload)
    assert response.status_code == HTTPStatus.OK
    token = response.json()["accessToken"]
    return {"email": registered_user["email"], "token": token}


@pytest.fixture
def valid_ingredients():
    """Возвращает список валидных ID ингредиентов (первые два)."""
    response = requests.get(f"{BASE_URL}{ENDPOINTS['INGREDIENTS']}")
    assert response.status_code == HTTPStatus.OK
    data = response.json()["data"]
    return [data[0]["_id"], data[1]["_id"]]
