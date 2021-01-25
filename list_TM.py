# Список транспортных средств (list TM - technical means)
import requests
import json
from settings import *
from eid_org import eid
from add_moduls import json_print_save


def search_list_TS():
    """
    Список ТС и их параметров ("flags": "0x00000001")
    :return:
    """
    params = {"spec": {"itemsType": "avl_unit", "propName": "sys_name", "propValueMask": "*",
                       "sortType": "sys_name"}, "force": 1, "flags": "0x00000001", "from": 0, "to": 0}
    data = json.dumps(params, separators=(',', ':'))
    req_string = f"{URL}{comand_str_items}{data}&sid={eid()}"
    # print(req_string)
    response = requests.get(req_string)
    # print("Количество ТС =", response.json()["totalItemsCount"], "\n")
    # print("Список ТС =", response.json(), "\n")
    # print(json_print(response.json()))
    json_print_save("ListTS.json", response.json())

    return

