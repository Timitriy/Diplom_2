import pytest
import requests
import allure

BASE_URL = "https://stellarburgers.nomoreparties.site/api"


@allure.feature("User Profile")
@pytest.mark.parametrize("field,value", [
    ("name", "New Name"),
])
def test_update_profile_authorized(authorized_user, field, value):
    with allure.step(f"Update user {field} with authorization"):
        headers = {"Authorization": authorized_user["token"]}
        payload = {field: value}
        response = requests.patch(f"{BASE_URL}/auth/user", headers=headers, json=payload)

        assert response.status_code == 200
        assert response.json()["success"] == True
        assert response.json()["user"][field] == value


@allure.feature("User Profile")
def test_update_profile_unauthorized():
    with allure.step("Try to update profile without authorization"):
        payload = {"name": "Unauthorized Update"}
        response = requests.patch(f"{BASE_URL}/auth/user", json=payload)

        assert response.status_code == 401
        assert response.json()["success"] == False
        assert response.json()["message"] == "You should be authorised"