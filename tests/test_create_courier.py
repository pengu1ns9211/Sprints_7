import allure
import requests
from const import MessageText, Const


class TestCreateCourier:

    @allure.title('Проверка создания курьера и успешной авторизации')
    def test_create_courier_and_login(self, create_courier, courier_helper):
        login, password, first_name = create_courier
        with allure.step("Проверяем успешный логин созданного курьера"):
            response = courier_helper.login_courier(login, password)
            assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
            response_json = response.json()
            assert MessageText.LOGIN_COURIER_SUCCESS_KEY in response_json, \
                f"В ответе нет ключа {MessageText.LOGIN_COURIER_SUCCESS_KEY}"
            assert isinstance(response_json[MessageText.LOGIN_COURIER_SUCCESS_KEY], int), \
                "id должен быть числом"
            assert response_json[MessageText.LOGIN_COURIER_SUCCESS_KEY] > 0, \
                "id должен быть положительным числом"

    @allure.title('Проверка невозможности создания двух одинаковых курьеров')
    def test_create_courier_twice(self, create_courier, courier_helper):
        login, password, first_name = create_courier
        with allure.step("Пытаемся создать курьера повторно с теми же данными"):
            response = courier_helper.create_courier(login, password, first_name)
            assert response.status_code == 409, f"Ожидался 409, получен {response.status_code}"

            response_json = response.json()
            assert "message" in response_json, "В ответе нет поля message"
            assert MessageText.CREATE_COURIER_TWICE in response_json["message"], \
                f"Ожидалось сообщение, содержащее '{MessageText.CREATE_COURIER_TWICE}', получено '{response_json['message']}'"

    @allure.title('Проверка создания курьера без логина')
    def test_create_courier_without_login(self, courier_helper):
        _, password, first_name = courier_helper.generate_courier_data()
        with allure.step("Пытаемся создать курьера без логина"):
            payload = {
                "password": password,
                "firstName": first_name
            }
            response = requests.post(Const.CREATE_COURIER, json=payload)
            assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"

            response_json = response.json()
            assert "message" in response_json, "В ответе нет поля message"
            assert response_json["message"] == MessageText.CREATE_COURIER_WITHOUT_LOGIN, \
                f"Ожидалось сообщение '{MessageText.CREATE_COURIER_WITHOUT_LOGIN}', получено '{response_json['message']}'"

    @allure.title('Проверка создания курьера без пароля')
    def test_create_courier_without_password(self, courier_helper):
        login, _, first_name = courier_helper.generate_courier_data()
        with allure.step("Пытаемся создать курьера без пароля"):
            payload = {
                "login": login,
                "firstName": first_name
            }
            response = requests.post(Const.CREATE_COURIER, json=payload)
            assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"

            response_json = response.json()
            assert "message" in response_json, "В ответе нет поля message"
            assert response_json["message"] == MessageText.CREATE_COURIER_WITHOUT_PASSWORD, \
                f"Ожидалось сообщение '{MessageText.CREATE_COURIER_WITHOUT_PASSWORD}', получено '{response_json['message']}'"

    @allure.title('Проверка создания курьера без имени')
    def test_create_courier_without_first_name(self, courier_helper):
        login, password, _ = courier_helper.generate_courier_data()
        with allure.step("Создаём курьера без имени"):
            payload = {"login": login, "password": password}
            response = requests.post(Const.CREATE_COURIER, json=payload)
            assert response.status_code == 201, f"Ожидался 201, получен {response.status_code}"

            response_json = response.json()
            assert MessageText.CREATE_COURIER_SUCCESS_KEY in response_json, \
                f"В ответе нет ключа {MessageText.CREATE_COURIER_SUCCESS_KEY}"
            assert response_json[MessageText.CREATE_COURIER_SUCCESS_KEY] is True, \
                f"Ожидалось True, получено {response_json[MessageText.CREATE_COURIER_SUCCESS_KEY]}"

        with allure.step("Удаляем созданного курьера"):
            courier_id = courier_helper.get_courier_id(login, password)
            if courier_id:
                delete_response = courier_helper.delete_courier(courier_id)
                assert delete_response.status_code == 200, f"Не удалось удалить курьера: {delete_response.status_code}"
