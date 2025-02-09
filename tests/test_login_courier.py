import allure
import requests
from urls import Urls
from data import ErrText

class TestLoginCouriers:

    allure.title('Тест на авторизацию курьера')
    def test_courier_can_login(self, courier):
        courier_data, _ = courier
        login_response = requests.post(Urls.LOGIN_COURIER_URL, json={
            "login": courier_data["login"],
            "password": courier_data["password"]
        })
        assert login_response.status_code == 200
        assert "id" in login_response.json()

    allure.title('Статус кода 404 и ошибка при вводе неверного логина')
    def test_login_fails_with_wrong_login(self, courier):
        courier_data, _ = courier
        invalid_login_data = {
            "login": "wrongLogin",  # Некорректный логин
            "password": courier_data["password"]
        }

        response = requests.post(Urls.LOGIN_COURIER_URL, json=invalid_login_data)
        assert response.status_code == 404
        assert response.json().get("message") == ErrText.ACCOUNT_NOT_FOUND

    allure.title('Статус кода 404 и ошибка при вводе неверного пароля')
    def test_login_fails_with_wrong_password(self, courier):
        courier_data, _ = courier
        invalid_password_data = {
            "login": courier_data["login"],
            "password": "wrongPassword"  # Некорректный пароль
        }

        response = requests.post(Urls.LOGIN_COURIER_URL, json=invalid_password_data)
        assert response.status_code == 404
        assert response.json().get("message") == ErrText.ACCOUNT_NOT_FOUND

    allure.title('Логин курьера без пароля')
    def test_login_fails_without_password(self, courier):
        courier_data, _ = courier
        response = requests.post(Urls.LOGIN_COURIER_URL, json={
            "login": courier_data["login"],
            "password": ""
        })

        assert response.status_code == 400
        assert response.json().get("message") == ErrText.INSUFFICIENT_LOGIN_INFORMATION

    allure.title('Логин курьера без логина')
    def test_login_fails_without_login(self, courier):
        courier_data, _ = courier
        response = requests.post(Urls.LOGIN_COURIER_URL, json={
            "login": "",
            "password": courier_data["password"]
        })

        assert response.status_code == 400
        assert response.json().get("message") == ErrText.INSUFFICIENT_LOGIN_INFORMATION
