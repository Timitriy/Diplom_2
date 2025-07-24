import pytest
import allure
import requests
import random
from http import HTTPStatus

from conftest import (
    BASE_URL, ENDPOINTS,
    ERR_USER_EXISTS, ERR_REQUIRED_FIELDS
)


@allure.feature("User Creation")
class TestUserCreation:

    def test_create_unique_user(self):
        with allure.step("Create user with unique email"):
            unique_email = f"test_{random.randint(1000, 9999)}@example.com"
            payload = {"email": unique_email, "password": "password123", "name": "Test User"}
            response = requests.post(f"{BASE_URL}{ENDPOINTS['REGISTER']}", json=payload)

            assert response.status_code == HTTPStatus.OK
            body = response.json()
            assert body["success"] is True
            assert "accessToken" in body

    def test_create_duplicate_user(self):
        with allure.step("Create user with static email to provoke duplicate error"):
            payload = {"email": "test_qwerty@example.com", "password": "password123", "name": "Test User"}
            response = requests.post(f"{BASE_URL}{ENDPOINTS['REGISTER']}", json=payload)

            assert response.status_code == HTTPStatus.FORBIDDEN
            body = response.json()
            assert body["success"] is False
            assert body["message"] == ERR_USER_EXISTS

    @allure.feature("User Creation")
    @allure.title("Create user without required field: {missing_field}")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_missing_field(self, missing_field):
        pass

    @allure.feature("User Creation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, missing_field):
        with allure.step(f"Create user without required field: {missing_field}"):
            payload = {"email": "test@example.com", "password": "password123", "name": "Test User"}
            del payload[missing_field]

            response = requests.post(f"{BASE_URL}{ENDPOINTS['REGISTER']}", json=payload)

            assert response.status_code == HTTPStatus.FORBIDDEN
            body = response.json()
            assert body["success"] is False
            assert body["message"] == ERR_REQUIRED_FIELDS
