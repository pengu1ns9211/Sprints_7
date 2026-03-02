import allure
import pytest
import requests
from const import MessageText, Const
from helpers import OrderHelpers


class TestCreateOrder:

    @pytest.mark.parametrize(
        "color, expected_status",
        [
            (["BLACK"], 201),  # Только BLACK
            (["GREY"], 201),   # Только GREY
            (["BLACK", "GREY"], 201),  # Оба цвета
            ([], 201)  # Без цвета
        ]
    )
    @allure.title('Создание заказа с цветом {color}')
    def test_create_order_with_color_parametrized(self, color, expected_status):
        """Параметризованный тест с разными вариантами цветов"""
        order_data = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 192 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 38",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": color
        }

        with allure.step(f'Отправка запроса на создание заказа с цветом {color}'):
            response = OrderHelpers.create_order(order_data)

        with allure.step('Проверка ответа'):
            assert response.status_code == expected_status, \
                f"Ожидался статус {expected_status}, получен {response.status_code}"

            response_json = response.json()
            assert MessageText.CREATE_ORDER_SUCCESS_KEY in response_json, \
                f"В ответе отсутствует поле {MessageText.CREATE_ORDER_SUCCESS_KEY}"
            assert isinstance(response_json[MessageText.CREATE_ORDER_SUCCESS_KEY], int), \
                f"Поле {MessageText.CREATE_ORDER_SUCCESS_KEY} должно быть числом"
            assert response_json[MessageText.CREATE_ORDER_SUCCESS_KEY] > 0, \
                f"{MessageText.CREATE_ORDER_SUCCESS_KEY} должен быть положительным числом"
