import allure
import requests
import pytest
from http import HTTPStatus

from conftest import (
    BASE_URL, ENDPOINTS,
    ERR_WRONG_CREDENTIALS
)

@allure.feature("User Login")
class TestUserLogin:

    def test_login_valid_user(self, registered_user):
        with allure.step("Login with valid credentials"):
            payload = {"email": registered_user["email"], "password": registered_user["password"]}
            response = requests.post(f"{BASE_URL}{ENDPOINTS['LOGIN']}", json=payload)

            assert response.status_code == HTTPStatus.OK
            body = response.json()
            assert body["success"] is True
            assert "accessToken" in body

    @pytest.mark.parametrize(
        "email,password",
        [
            ("wrong@example.com", "password123"),
            ("test@example.com", "wrongpassword"),
            ("", "password123"),
            ("test@example.com", "")
        ]
    )
    def test_login_invalid_credentials(self, email, password):
        with allure.step(f"Login with invalid credentials: {email}/{password}"):
            payload = {"email": email, "password": password}
            response = requests.post(f"{BASE_URL}{ENDPOINTS['LOGIN']}", json=payload)

            assert response.status_code == HTTPStatus.UNAUTHORIZED
            body = response.json()
            assert body["success"] is False
            assert body["message"] == ERR_WRONG_CREDENTIALS