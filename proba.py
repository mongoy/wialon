import requests
import json
from settings import *

from add_moduls import json_print_save, json_print


def prb1(eid_org):
    """
    Список ТС и их параметров ("flags": "0x00000001")
    :return:
    """
    params = {"spec": {"itemsType": 'avl_unit_group', "propName": "sys_name", "propValueMask": "*",
                       "sortType": "sys_name"}, "force": 1, "flags": "0x00000001", "from": 0, "to": 0}
    data = json.dumps(params, separators=(',', ':'))
    req_string = f"{URL}{comand_str_items}{data}&sid={eid_org}"
    print(req_string)
    response = requests.get(req_string)
    # print("Количество ТС =", response.json()["totalItemsCount"], "\n")
    print("Список групп ТС =", json_print(response.json()), "\n")
    # for c, row in enumerate(response.json()["items"]):
    #     # print(row["nm"], "\n")
    #     if row["nm"] == "Камаз к413ху":
    #         print(json_print(row), "\n")
    # print(json_print(response.json()["items"][0]))
    # json_print_save("OUT\\ListTS.json", response.json())
    #
    # for row in response.json()["items"]:
    #     print(row, "\n")
    # print("Всего :", response.json()["totalItemsCount"], "транспортных средств")


    return



