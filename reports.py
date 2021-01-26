# Отчёты
import requests
import json
from settings import *
from add_moduls import DataTime_to_sec, json_print_save, json_print


def search_reports(eid_org):
    """
    Список отчётов пользователя
    :return:
    """
    params = {"spec": {"itemsType": "avl_resource", "propName": "reporttemplates", "propValueMask": "*",
                       "sortType": "reporttemplates"}, "force": 1, "flags": "0x00002001", "from": 0, "to": 0}
    data = json.dumps(params, separators=(',', ':'))
    req_string = f"{URL}{comand_str_items}{data}&sid={eid_org}"
    # print(req_string)
    response = requests.get(req_string)
    # print("Отчёт =", response.json(), "\n")
    # print("Отчёты =", json_print(response.json()["items"]))
    json_print_save("OUT\\reports.json", response.json())
    return


def report(eid_org):
    """
    Получение пробега  и данных по расходу топлива ("reportTemplateId": 1) за период
    ID 21345040 - "KGUP75"
    ТС "Камаз к678ст" ID 21369701 20.01.2021 00:00 - 21.01.2021 06:31
    :return:
    """
    dt = DataTime_to_sec(2021, 1, 20, 0, 0, 0)
    date_first = dt  # Дата начала
    dt = DataTime_to_sec(2021, 1, 21, 14, 0, 0)
    date_last = dt  # Дата окончания
    params = {"reportResourceId": 21345040, "reportTemplateId": 1, "reportObjectId": 21369701, "reportObjectSecId": 0,
              "interval": {"from": date_first, "to": + date_last, "flags": 0}}
    data = json.dumps(params, separators=(',', ':'))
    req_string = f"{URL}{comand_str_report}{data}&sid={eid_org}"
    # print(req_string)
    response = requests.get(req_string)
    # print("Отчёт =", response.json(), "\n")
    # на экран
    json_print(response.json())
    # в файл
    json_print_save("OUT\\RepTC_1.json", response.json())

    # Результаты отчёта
    params = {'tableIndex': 0, "indexFrom": 0, "indexTo": 0}
    data = json.dumps(params, separators=(',', ':'))
    req_string = f"{URL}{comand_str_rep_data}{data}&sid={eid_org}"
    # print(req_string)
    response = requests.get(req_string)
    print("Отчёт (данные) =", response.json(), "\n")
    # на экран
    json_print(response.json())
    # в файл
    json_print_save("OUT\\RepTC_2.json", response.json())

    return
