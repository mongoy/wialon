# Список транспортных средств (list TM - technical means)
import requests
import json
from settings import *
from add_moduls import json_print_save


def search_list_TS(eid_org):
    """
    Список ТС и их параметров ("flags": "0x00000001")
    :return:
    """
    params = {"spec": {"itemsType": "avl_unit", "propName": "sys_name", "propValueMask": "*",
                       "sortType": "sys_name"}, "force": 1, "flags": "0x00000001", "from": 0, "to": 0}
    data = json.dumps(params, separators=(',', ':'))
    req_string = f"{URL}{comand_str_items}{data}&sid={eid_org}"
    # print(req_string)
    response = requests.get(req_string)
    # print("Количество ТС =", response.json()["totalItemsCount"], "\n")
    # print("Список ТС =", response.json(), "\n")
    # print(json_print(response.json()))
    json_print_save("OUT\\ListTS.json", response.json())

    return


def search_TS(id_TS, eid_org):
    """
    Поиск элемента по ID
    :return:
    """
    params = {"id": id_TS, "flags": 1025}
    data = json.dumps(params, separators=(',', ':'))
    req_string = f"{URL}{comand_str_item}{data}&sid={eid_org}"
    # print(req_string)
    response = requests.get(req_string)

    # print("Список параметров элемента =", response.json(), "\n")
    # print(len(response.json()["item"]))

    json_print_save("OUT\\OneID.json", response.json())

    return

