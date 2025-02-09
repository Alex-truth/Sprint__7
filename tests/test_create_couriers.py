import allure
import requests
from urls import Urls
from data import ErrText
from conftest import generate_random_string

class TestCreateCourier:
    allure.title('Тест на создание курьера и получение статус кода 201 и сообщения {"ok": True}')
    def test_create_courier_success(self, courier):
        courier_data, response = courier
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    allure.title('При создании двух курьеров с одинаковыми данными получаем статус кода 409 и ошибку')
    def test_cannot_create_duplicate_courier(self, courier):
        courier_data, response = courier
        duplicate_response = requests.post(Urls.CREATE_COURIER_URL, json=courier_data)
        assert duplicate_response.status_code == 409
        assert duplicate_response.json().get("message") == ErrText.USERNAME_IS_USE

    allure.title('Статус код 400 и ошибка при создании курьера без логина')
    def test_create_courier_without_login(self):
        invalid_courier_data = {
            "password": generate_random_string(),
            "firstName": generate_random_string(6)
        }

        response = requests.post(Urls.CREATE_COURIER_URL, json=invalid_courier_data)
        assert response.status_code == 400
        assert response.json().get("message") == ErrText.NOT_ENOUGH_DATA_TO_CREATE_ACC

    allure.title('Статус код 400 и ошибка при создании курьера без пароля')
    def test_create_courier_without_password(self):
        invalid_courier_data = {
            "login": generate_random_string(),
            "firstName": generate_random_string(6)
        }

        response = requests.post(Urls.CREATE_COURIER_URL, json=invalid_courier_data)
        assert response.status_code == 400
        assert response.json().get("message") == ErrText.NOT_ENOUGH_DATA_TO_CREATE_ACC

    allure.title('Нельзя создать курьера с уже существующим логином')
    def test_cannot_create_duplicate_login(self, courier):
        courier_data, _ = courier  # Берём данные созданного курьера

        duplicate_courier_data = {
            "login": courier_data["login"],  # Используем тот же логин
            "password": generate_random_string(),
            "firstName": generate_random_string(6)
        }

        response = requests.post(Urls.CREATE_COURIER_URL, json=duplicate_courier_data)
        assert response.status_code == 409
        assert response.json().get("message") == ErrText.USERNAME_IS_USE
