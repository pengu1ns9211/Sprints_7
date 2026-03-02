import allure
import requests
from const import MessageText, Const


class TestGetOrderList:
    @allure.title('Проверка получения списка заказов')
    def test_get_order_list(self):
        with allure.step('Отправка GET запроса на получение списка заказов'):
            response = requests.get(Const.ORDER_LIST)
            allure.attach(response.text, name='Response body', attachment_type=allure.attachment_type.JSON)

        with allure.step('Проверка кода ответа и структуры JSON'):
            assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

            response_json = response.json()

            # Проверяем наличие ключа 'orders' в ответе
            assert MessageText.LIST_ORDERS_KEY in response_json, \
                f"В ответе отсутствует ключ '{MessageText.LIST_ORDERS_KEY}'"

            # Проверяем, что значение по ключу 'orders' является списком
            orders_list = response_json[MessageText.LIST_ORDERS_KEY]
            assert isinstance(orders_list, list), \
                f"Значение '{MessageText.LIST_ORDERS_KEY}' должно быть списком, получен {type(orders_list)}"

            # Проверяем структуру первых 3 заказов (или всех, если их меньше)
            if orders_list:
                # Проверяем не более 3 заказов для оптимизации
                orders_to_check = orders_list[:3]
                for order in orders_to_check:
                    assert isinstance(order, dict), f"Заказ должен быть словарем, получен {type(order)}"
                    # Проверяем только ключевые поля
                    assert "id" in order, "В заказе отсутствует поле id"
                    assert "track" in order, "В заказе отсутствует поле track"
                    assert "firstName" in order, "В заказе отсутствует поле firstName"
