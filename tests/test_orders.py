import pytest
import allure
import requests
from http import HTTPStatus

from conftest import (
    BASE_URL, ENDPOINTS,
    ERR_NO_INGREDIENTS
)


@allure.feature("Orders")
class TestOrders:

    def test_create_order_authorized(self, authorized_user, valid_ingredients):
        with allure.step("Create order with authorization and valid ingredients"):
            headers = {"Authorization": authorized_user["token"]}
            payload = {"ingredients": valid_ingredients}
            response = requests.post(f"{BASE_URL}{ENDPOINTS['ORDERS']}", headers=headers, json=payload)

            assert response.status_code == HTTPStatus.OK
            body = response.json()
            assert body["success"] is True
            assert "order" in body

    def test_create_order_unauthorized(self, valid_ingredients):
        with allure.step("Try to create order without authorization"):
            payload = {"ingredients": valid_ingredients}
            response = requests.post(f"{BASE_URL}{ENDPOINTS['ORDERS']}", json=payload)

            assert response.status_code == HTTPStatus.OK
            assert response.json()["success"] is True

    def test_create_order_no_ingredients(self, authorized_user):
        with allure.step("Try to create order without ingredients"):
            headers = {"Authorization": authorized_user["token"]}
            payload = {"ingredients": []}
            response = requests.post(f"{BASE_URL}{ENDPOINTS['ORDERS']}", headers=headers, json=payload)

            assert response.status_code == HTTPStatus.BAD_REQUEST
            body = response.json()
            assert body["success"] is False
            assert body["message"] == ERR_NO_INGREDIENTS

    def test_create_order_invalid_ingredients(self, authorized_user):
        with allure.step("Try to create order with invalid ingredients"):
            headers = {"Authorization": authorized_user["token"]}
            payload = {"ingredients": ["invalid_hash1", "invalid_hash2"]}
            response = requests.post(f"{BASE_URL}{ENDPOINTS['ORDERS']}", headers=headers, json=payload)

            # По текущему API иногда 500
            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

    def test_get_user_orders(self, authorized_user):
        with allure.step("Get user orders with authorization"):
            headers = {"Authorization": authorized_user["token"]}
            response = requests.get(f"{BASE_URL}{ENDPOINTS['ORDERS']}", headers=headers)

            assert response.status_code == HTTPStatus.OK
            body = response.json()
            assert body["success"] is True
            assert "orders" in body
