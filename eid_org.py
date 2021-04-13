import requests
import json
from settings import *
from settings_org import TOKEN
from add_moduls import json_print_save


# строка запроса
def req_string(params, svc):
    """
    Формируем строку запроса
    :param params: пармметры команды
    :param svc: комнда
    :return: строка запроса
    """
    data = json.dumps(params, separators=(',', ':'))
    req_text = f"{URL}{svc}{data}"
    return req_text


# LOGIN API
def eid():
    """
    Вход и получение id-сессии
    :return: ID сессии
    """
    params = {'token': TOKEN, 'operateAs': '', 'fl': 2}  # fl = 1(2), 1-сокращенная, 2-полная информация
    response = requests.get(req_string(params, command_login))
    print("\n", "код ответа =", response, "\n")

    # Вывод ответа (response)
    # print("response:\n{}\n".format(response))
    # print("response.url:\n{}\n".format(response.url))                  # Посмотреть формат URL (с параметрами)
    # print("response.headers:\n{}\n".format(response.headers))          # Header of the request
    # print("response.status_code:\n{}\n".format(response.status_code))  # Получить код ответа
    # print("response.text:\n{}\n".format(response.text))                # Text Output
    # print("response.encoding:\n{}\n".format(response.encoding))        # Узнать, какую кодировку использует Requests
    # print("response.content:\n{}\n".format(response.content))          # В бинарном виде
    # print("response.json():\n{}\n".format(response.json()))            # JSON Output
    # json_print_save("DOC\\Main_Response.json", response.json())

    # идентификатор сессии
    dict_info = dict(response.json())
    eid_org = dict_info['eid']
    print("ID сессии =", eid_org, "\n")
    return eid_org


# LOGOUT API
def logout(eid_org):
    """
    Закрытие сессии
    :param eid_org: ID сессии
    :return:
    """
    req_string = f"{URL}{command_out}{eid_org}"
    response = requests.get(req_string)
    print("\n", "Сессия закрыта", response.json())
    return


