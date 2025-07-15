import pytest
import requests
import allure

BASE_URL = "https://stellarburgers.nomoreparties.site/api"

import pytest
import requests
import allure

BASE_URL = "https://stellarburgers.nomoreparties.site/api"


@allure.feature("User Login")
def test_login_valid_user(registered_user):
    with allure.step("Login with valid credentials"):
        payload = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=payload)

        assert response.status_code == 200
        assert response.json()["success"] == True
        assert "accessToken" in response.json()


@allure.feature("User Login")
@pytest.mark.parametrize("email,password,expected_message", [
    ("wrong@example.com", "password123", "email or password are incorrect"),
    ("test@example.com", "wrongpassword", "email or password are incorrect"),
    ("", "password123", "email or password are incorrect"),
    ("test@example.com", "", "email or password are incorrect")
])
def test_login_invalid_credentials(email, password, expected_message):
    with allure.step(f"Login with invalid credentials: {email}/{password}"):
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=payload)

        assert response.status_code == 401
        assert response.json()["success"] == False
        assert response.json()["message"] == expected_message