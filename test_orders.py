import pytest
import requests
import allure

BASE_URL = "https://stellarburgers.nomoreparties.site/api"


@allure.feature("Orders")
def test_create_order_authorized(authorized_user, valid_ingredients):
    with allure.step("Create order with authorization and valid ingredients"):
        headers = {"Authorization": authorized_user["token"]}
        payload = {"ingredients": valid_ingredients}
        response = requests.post(f"{BASE_URL}/orders", headers=headers, json=payload)

        assert response.status_code == 200
        assert response.json()["success"] == True
        assert "order" in response.json()


@allure.feature("Orders")
def test_create_order_unauthorized(valid_ingredients):
    with allure.step("Try to create order without authorization"):
        payload = {"ingredients": valid_ingredients}
        response = requests.post(f"{BASE_URL}/orders", json=payload)

        assert response.status_code == 200
        assert response.json()["success"] == True


@allure.feature("Orders")
def test_create_order_no_ingredients(authorized_user):
    with allure.step("Try to create order without ingredients"):
        headers = {"Authorization": authorized_user["token"]}
        payload = {"ingredients": []}
        response = requests.post(f"{BASE_URL}/orders", headers=headers, json=payload)

        assert response.status_code == 400
        assert response.json()["success"] == False
        assert response.json()["message"] == "Ingredient ids must be provided"


@allure.feature("Orders")
def test_create_order_invalid_ingredients(authorized_user):
    with allure.step("Try to create order with invalid ingredients"):
        headers = {"Authorization": authorized_user["token"]}
        payload = {"ingredients": ["invalid_hash1", "invalid_hash2"]}
        response = requests.post(f"{BASE_URL}/orders", headers=headers, json=payload)

        assert response.status_code == 500


@allure.feature("Orders")
def test_get_user_orders(authorized_user):
    with allure.step("Get user orders with authorization"):
        headers = {"Authorization": authorized_user["token"]}
        response = requests.get(f"{BASE_URL}/orders", headers=headers)

        assert response.status_code == 200
        assert response.json()["success"] == True
        assert "orders" in response.json()