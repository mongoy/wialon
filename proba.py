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
    req_string = f"{URL}{command_core_search_items}{data}&sid={eid_org}"
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


def prb2(eid_org):
    date_first, date_last = [1611068400, 1611241200]
    params = {"reportResourceId": 21345040, "reportTemplateId": 1, "reportObjectId": 21345174,
              "reportObjectSecId": 0, "interval": {"from": date_first, "to": + date_last, "flags": 0}}
    data = json.dumps(params, separators=(',', ':'))
    req_string = f"{URL}{command_report_exec_report}{data}&sid={eid_org}"
    # print(req_string, "\n")
    response = requests.get(req_string)

    if len(response.json()["reportResult"]["tables"]) > 0:
        # Наличие данных за период
        # на экран
        json_print(response.json())
        print(len(response.json()["reportResult"]["tables"]))
        # json_print(response.json()["reportResult"]["tables"])
        # unit_trips = (response.json()["reportResult"]["tables"][0]["label"],
        #               response.json()["reportResult"]["tables"][0]["header"],
        #               response.json()["reportResult"]["tables"][0]["total"],
        #               response.json()["reportResult"]["tables"][1]["label"],
        #               response.json()["reportResult"]["tables"][1]["header"],
        #               response.json()["reportResult"]["tables"][1]["total"]
        #               )
        #
        # print(unit_trips)
    else:
        print("Нет данных за период")

