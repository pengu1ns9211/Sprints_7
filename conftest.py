import pytest
import requests
from const import Const
from helpers import CourierHelpers


@pytest.fixture
def courier_helper():
    """Фикстура для работы с курьерами"""
    return CourierHelpers()


@pytest.fixture
def create_courier(courier_helper):
    """Фикстура создает курьера и удаляет его после теста"""
    login, password, first_name = courier_helper.generate_courier_data()
    response = courier_helper.create_courier(login, password, first_name)

    yield login, password, first_name

    # Очистка после теста
    courier_id = courier_helper.get_courier_id(login, password)
    if courier_id:
        courier_helper.delete_courier(courier_id)
