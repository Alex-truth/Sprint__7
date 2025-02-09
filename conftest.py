import allure
import pytest
import requests
from helpers import generate_random_string
from urls import Urls

allure.title('Создаёт курьера перед тестом и удаляет после')
@pytest.fixture
def courier():
    courier_data = {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string(6)
    }

    response = requests.post(Urls.CREATE_COURIER_URL, json=courier_data)

    yield courier_data, response  # Передаём в тест

    # Удаляем курьера после теста
    login_response = requests.post(Urls.LOGIN_COURIER_URL, json={
        "login": courier_data["login"],
        "password": courier_data["password"]
    })

    if login_response.status_code == 200 and "id" in login_response.json():
        courier_id = login_response.json()["id"]
        requests.delete(f"{Urls.CREATE_COURIER_URL}/{courier_id}")
