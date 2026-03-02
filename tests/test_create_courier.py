import allure
import requests
from const import MessageText, Const

class TestCreateCourier:
    @allure.title('Проверка создания курьера со всеми обязательными полями')
    def test_create_courier(self, create_courier):
        login, password, first_name = create_courier
        with allure.step("Проверяем успешный логин созданного курьера"):
            response = requests.post(
                Const.LOGIN_COURIER,
                json={"login": login, "password": password}
            )
            assert response.status_code == 200, f"Не удалось залогиниться: {response.text}"

    @allure.title('Проверка невозможности создания двух одинаковых курьеров')
    def test_create_courier_twice(self, create_courier):
        login, password, first_name = create_courier
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        with allure.step("Пытаемся создать курьера повторно с теми же данными"):
            response = requests.post(Const.CREATE_COURIER, json=payload)
            assert response.status_code == 409, f"Ожидался 409, получен {response.status_code}"
            assert MessageText.CREATE_COURIER_TWICE in response.text

    @allure.title('Проверка создания курьера без логина')
    def test_create_courier_without_login(self, helpers):
        login, password, first_name = helpers.generate_data()
        payload = {
            "password": password,
            "firstName": first_name
        }
        with allure.step("Пытаемся создать курьера без логина"):
            response = requests.post(Const.CREATE_COURIER, json=payload)
            assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
            assert MessageText.CREATE_COURIER_WITHOUT_LOGIN in response.text

    @allure.title('Проверка создания курьера без пароля')
    def test_create_courier_without_password(self, helpers):
        login, password, first_name = helpers.generate_data()
        payload = {
            "login": login,
            "firstName": first_name
        }
        with allure.step("Пытаемся создать курьера без пароля"):
            response = requests.post(Const.CREATE_COURIER, json=payload)
            assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
            assert MessageText.CREATE_COURIER_WITHOUT_PASSWORD in response.text

    @allure.title('Проверка создания курьера без имени')
    def test_create_courier_without_first_name(self, helpers):
        login, password, _ = helpers.generate_data()
        payload = {
            "login": login,
            "password": password
        }

        with allure.step("Создаём курьера без имени"):
            response = requests.post(Const.CREATE_COURIER, json=payload)
            assert response.status_code == 201, f"Ожидался 201, получен {response.status_code}"
            assert MessageText.CREATE_COURIER in response.text

        with allure.step("Удаляем созданного курьера"):
            helpers.delete_courier(login, password)
