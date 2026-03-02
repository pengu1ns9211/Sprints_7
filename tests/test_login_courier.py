import allure
import requests
from const import MessageText, Const


class TestLoginCourier:

    @allure.title('Проверка авторизации курьера')
    def test_login_courier(self, create_courier, courier_helper):
        login, password, _ = create_courier
        with allure.step('Отправка запроса на авторизацию курьера с валидными данными'):
            response = courier_helper.login_courier(login, password)

        with allure.step('Проверка успешной авторизации'):
            assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

            response_json = response.json()
            assert MessageText.LOGIN_COURIER_SUCCESS_KEY in response_json, \
                f"В ответе нет ключа {MessageText.LOGIN_COURIER_SUCCESS_KEY}"
            assert isinstance(response_json[MessageText.LOGIN_COURIER_SUCCESS_KEY], int), \
                "id должен быть числом"
            assert response_json[MessageText.LOGIN_COURIER_SUCCESS_KEY] > 0, \
                "id должен быть положительным числом"

    @allure.title('Проверка авторизации курьера без логина')
    def test_login_courier_without_login(self, create_courier, courier_helper):
        _, password, _ = create_courier
        with allure.step('Отправка запроса на авторизацию без логина'):
            # Используем прямые запросы, так как хелпер требует оба поля
            response = requests.post(Const.LOGIN_COURIER, json={
                "login": '',
                "password": password
            })

        with allure.step('Проверка ответа об ошибке'):
            assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"

            response_json = response.json()
            assert "message" in response_json, "В ответе нет поля message"
            assert response_json["message"] == MessageText.LOGIN_COURIER_WITHOUT_DATA, \
                f"Ожидалось сообщение '{MessageText.LOGIN_COURIER_WITHOUT_DATA}', получено '{response_json['message']}'"

    @allure.title('Проверка авторизации курьера без пароля')
    def test_login_courier_without_password(self, create_courier, courier_helper):
        login, _, _ = create_courier
        with allure.step('Отправка запроса на авторизацию без пароля'):
            response = requests.post(Const.LOGIN_COURIER, json={
                "login": login,
                "password": ''
            })

        with allure.step('Проверка ответа об ошибке'):
            assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"

            response_json = response.json()
            assert "message" in response_json, "В ответе нет поля message"
            assert response_json["message"] == MessageText.LOGIN_COURIER_WITHOUT_DATA, \
                f"Ожидалось сообщение '{MessageText.LOGIN_COURIER_WITHOUT_DATA}', получено '{response_json['message']}'"

    @allure.title('Проверка авторизации курьера без логина и пароля')
    def test_login_courier_without_data(self, courier_helper):
        with allure.step('Отправка запроса на авторизацию без логина и пароля'):
            response = requests.post(Const.LOGIN_COURIER, json={
                "login": '',
                "password": '',
            })

        with allure.step('Проверка ответа об ошибке'):
            assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"

            response_json = response.json()
            assert "message" in response_json, "В ответе нет поля message"
            assert response_json["message"] == MessageText.LOGIN_COURIER_WITHOUT_DATA, \
                f"Ожидалось сообщение '{MessageText.LOGIN_COURIER_WITHOUT_DATA}', получено '{response_json['message']}'"

    @allure.title('Проверка авторизации с несуществующими данными')
    def test_login_courier_fake_data(self, courier_helper):
        with allure.step('Отправка запроса на авторизацию с несуществующими данными'):
            response = requests.post(Const.LOGIN_COURIER, json={
                "login": 'victor',
                "password": 'qwertyuiopasd',
            })

        with allure.step('Проверка ответа об ошибке'):
            assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}"

            response_json = response.json()
            assert "message" in response_json, "В ответе нет поля message"
            assert response_json["message"] == MessageText.LOGIN_COURIER_FAKE_DATA, \
                f"Ожидалось сообщение '{MessageText.LOGIN_COURIER_FAKE_DATA}', получено '{response_json['message']}'"
