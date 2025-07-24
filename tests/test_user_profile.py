import pytest
import allure
import requests
from http import HTTPStatus

from conftest import (
    BASE_URL, ENDPOINTS,
    ERR_UNAUTHORIZED
)


@allure.feature("User Profile")
class TestUserProfile:

    @pytest.mark.parametrize("field,value", [("name", "New Name")])
    def test_update_profile_authorized(self, authorized_user, field, value):
        with allure.step(f"Update user {field} with authorization"):
            headers = {"Authorization": authorized_user["token"]}
            payload = {field: value}
            response = requests.patch(f"{BASE_URL}{ENDPOINTS['USER']}", headers=headers, json=payload)

            assert response.status_code == HTTPStatus.OK
            body = response.json()
            assert body["success"] is True
            assert body["user"][field] == value

    def test_update_profile_unauthorized(self):
        with allure.step("Try to update profile without authorization"):
            payload = {"name": "Unauthorized Update"}
            response = requests.patch(f"{BASE_URL}{ENDPOINTS['USER']}", json=payload)

            assert response.status_code == HTTPStatus.UNAUTHORIZED
            body = response.json()
            assert body["success"] is False
            assert body["message"] == ERR_UNAUTHORIZED
