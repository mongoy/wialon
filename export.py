# Экспорт в файл: excel,
import requests
import json
from settings import *
from add_moduls import DataTime_to_sec, json_print_save, json_print


def export_to_xlsx(eid_org):
    """
    Экспорт в excel
    :return:
    """
    params = {"spec": {
            "itemsType": "avl_unit",
            "propName": "sys_name",
            "propValueMask": "*",
            "sortType": "sys_name"
            },
            "force": 1,
            "flags": "0x0001",
            }
    data = json.dumps(params, separators=(',', ':'))
    req_string = f"{URL}{comand_str_items}{data}&sid={eid_org}"
    print(req_string)
    response = requests.get(req_string)
    print("=", response.json(), "\n")
    return
