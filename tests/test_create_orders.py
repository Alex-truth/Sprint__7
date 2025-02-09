import allure
import pytest
import requests
from urls import Urls
from data import (
    order_black,
    order_gray,
    order_black_and_gray,
    order_without_color
)

class TestCreateOrder:

    allure.title('Создание заказа с разным набором цветов и тело ответа содержит "track"')
    @pytest.mark.parametrize("order_data", [
        order_black,
        order_gray,
        order_black_and_gray,
        order_without_color])
    def test_create_order(self, order_data):
        response = requests.post(Urls.ORDER_URL, json=order_data)
        assert response.status_code == 201
        assert "track" in response.json()


    allure.title('В тело ответа возвражается список заказа')
    def test_get_orders_list(self):
        response = requests.get(Urls.ORDER_URL)
        assert response.status_code == 200
        response_data = response.json()
        assert "orders" in response_data and isinstance(response_data["orders"], list)
        assert len(response_data["orders"]) > 0

