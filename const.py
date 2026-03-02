class Const:
    MAIN_URL = 'http://qa-scooter.praktikum-services.ru'
    CREATE_COURIER = f'{MAIN_URL}/api/v1/courier'
    LOGIN_COURIER = f'{MAIN_URL}/api/v1/courier/login'
    CREATE_ORDER = f'{MAIN_URL}/api/v1/orders'
    ORDER_LIST = f'{MAIN_URL}/api/v1/orders'
    DELETE_COURIER = f'{MAIN_URL}/api/v1/courier/'
    GET_ORDER_TRACK = f'{MAIN_URL}/api/v1/orders/track'
    TAKE_ORDER = f'{MAIN_URL}/api/v1/orders/accept/'


class MessageText:
    # Успешные ответы (ключи)
    CREATE_COURIER_SUCCESS_KEY = "ok"
    LOGIN_COURIER_SUCCESS_KEY = "id"
    CREATE_ORDER_SUCCESS_KEY = "track"
    TAKE_ORDER_SUCCESS_KEY = "ok"
    LIST_ORDERS_KEY = "orders"
    GET_ORDER_KEY = "order"

    # Сообщения об ошибках
    CREATE_COURIER_TWICE = 'Этот логин уже используется. Попробуйте другой.'
    CREATE_COURIER_WITHOUT_LOGIN = 'Недостаточно данных для создания учетной записи'
    CREATE_COURIER_WITHOUT_PASSWORD = 'Недостаточно данных для создания учетной записи'

    LOGIN_COURIER_WITHOUT_DATA = 'Недостаточно данных для входа'
    LOGIN_COURIER_FAKE_DATA = 'Учетная запись не найдена'

    TAKE_ORDER_FAKE_ID = 'Заказа с таким id не существует'
    TAKE_ORDER_FAKE_ID_COURIER = 'Курьера с таким id не существует'
    TAKE_ORDER_FAKE_TWICE = 'Этот заказ уже в работе'
    TAKE_ORDER_WITHOUT_ID_COURIER_ORDER = 'Недостаточно данных для поиска'

    GET_ORDER_WITHOUT_TRACK = 'Недостаточно данных для поиска'
    GET_ORDER_FAKE_TRACK = 'Заказ не найден'
