import pytest
import requests
import allure
import random

BASE_URL = "https://stellarburgers.nomoreparties.site/api"

@allure.feature('User Creation')
def test_create_unique_user():
    with allure.step("Create user with unique email"):
        unique_email = f'test_{random.randint(1000, 9999)}@example.com'
        payload = {
            'email': unique_email,
            'password': 'password123',
            'name': 'Test User'
        }

        response = requests.post(f'{BASE_URL}/auth/register', json=payload)

        assert response.status_code == 200
        assert response.json()['success'] == True
        assert "accessToken" in response.json()


@allure.feature('User Creation')
def test_create_duplicate_user():
    with allure.step("Create user with unique email"):
        unique_email = f'test_qwerty@example.com'
        payload = {
            'email': unique_email,
            'password': 'password123',
            'name': 'Test User'
        }

        response = requests.post(f'{BASE_URL}/auth/register', json=payload)

        assert response.status_code == 403
        assert response.json()['success'] == False
        assert response.json()['message'] == "User already exists"


@allure.feature('User Creation')
@pytest.mark.parametrize('missing_field', ['email', 'password', 'name'])
def test_create_user_missing_field(missing_field):
    with allure.step(f"Create user without required field: {missing_field}"):
        payload = {
            'email': "test@example.com",
            'password': 'password123',
            'name': 'Test User'
        }

        del payload[missing_field]
        response = requests.post(f'{BASE_URL}/auth/register', json=payload)

        assert response.status_code == 403
        assert response.json()["success"] == False
        assert response.json()["message"] == "Email, password and name are required fields"

