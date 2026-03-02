import allure
import requests
import random
import string
from const import Const


class CourierHelpers:
    """Класс с методами для работы с курьерами"""

    @staticmethod
    def generate_random_string(length):
        """Генерирует случайную строку заданной длины"""
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def generate_courier_data(self):
        """Генерирует данные для курьера"""
        login = self.generate_random_string(10)
        password = self.generate_random_string(10)
        first_name = self.generate_random_string(10)
        return login, password, first_name

    @allure.step('Создаем курьера')
    def create_courier(self, login, password, first_name):
        """Создает курьера и возвращает ответ"""
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        return requests.post(Const.CREATE_COURIER, json=payload)

    @allure.step('Логинимся курьером')
    def login_courier(self, login, password):
        """Логинит курьера и возвращает ответ"""
        payload = {
            "login": login,
            "password": password
        }
        return requests.post(Const.LOGIN_COURIER, json=payload)

    @allure.step('Удаляем курьера')
    def delete_courier(self, courier_id):
        """Удаляет курьера по id"""
        return requests.delete(f'{Const.DELETE_COURIER}/{courier_id}')

    @allure.step('Получаем id курьера')
    def get_courier_id(self, login, password):
        """Получает id курьера после логина"""
        response = self.login_courier(login, password)
        if response.status_code == 200:
            return response.json().get("id")
        return None


class OrderHelpers:
    """Класс с методами для работы с заказами"""

    @staticmethod
    def create_order(order_data):
        """Создает заказ и возвращает ответ"""
        return requests.post(Const.CREATE_ORDER, json=order_data)

    @staticmethod
    def get_order_track(response):
        """Получает track из ответа"""
        return response.json().get("track")
