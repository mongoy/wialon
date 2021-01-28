# Список транспортных средств (list TM - technical means)
import json
import xlsxwriter
import requests

from add_moduls import json_print_save
from settings import *


def search_list_TS(eid_org):
    """
    Список ТС и их параметров ("flags": "0x00000001")
    :param eid_org: ID - сессии
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
    dict_TM = {}  # словарь с названиями транспортных средств
    for c, row in enumerate(response.json()["items"]):
        dict_TM[row["id"]] = row["nm"]
    #     # print(row["nm"], "\n")
    #     if row["nm"] == "Камаз к413ху":
    #         dict_TM[row["id"]] = row["nm"]
    #         print(json_print(row), "\n")
    #         # print(dict_TM)
    # # print(json_print(response.json()["items"][0]))
    # json_print_save("OUT\\ListTS.json", response.json())
    #
    # for row in response.json()["items"]:
    #     print(row, "\n")
    # print("Всего :", response.json()["totalItemsCount"], "транспортных средств")

    return dict_TM


def search_list_group_TS(eid_org):
    """
    Список групп транспортных средств + списки транспортных средств по группам
    :param eid_org: ID - сессии
    :return:
    """
    # Выгрузка списка транспортных средств
    dict_tm = search_list_TS(eid_org)

    # Выгрузка списка групп
    params = {"spec": {"itemsType": 'avl_unit_group', "propName": "sys_name", "propValueMask": "*",
                       "sortType": "sys_name"}, "force": 1, "flags": "0x00000001", "from": 0, "to": 0}
    data = json.dumps(params, separators=(',', ':'))
    req_string = f"{URL}{comand_str_items}{data}&sid={eid_org}"
    print(req_string)
    response = requests.get(req_string)
    print("Количество групп ТС =", response.json()["totalItemsCount"], "\n")
    # print("Список групп ТС =", json_print(response.json()["items"]), "\n")
    # json_print_save("OUT\\ListGroupTS.json", response.json()["items"])

    # Создайте рабочую книгу и добавьте рабочий лист.
    workbook = xlsxwriter.Workbook('OUT\\List_group_TM.xlsx')
    worksheet = workbook.add_worksheet('Транспортные средства')
    # Начните с первой ячейки. Строки и столбцы индексируются нулем.
    row = 0
    col = 0

    # Формирование списка ТС по группам и запись в файл
    worksheet.write(row, col + 1, "ID")
    worksheet.write(row, col + 2, "Наименование")
    row += 1
    for group_TM in response.json()["items"]:
        print("Группа:", group_TM["nm"])
        print("  ТС:")
        worksheet.write(row, col, "Группа:")
        worksheet.write(row, col + 1, group_TM["nm"])
        row += 1
        worksheet.write(row, col, "  ТС:")
        row += 1
        for c, tm in enumerate(group_TM["u"]):
            print("  ", tm, dict_tm[tm])
            worksheet.write(row, col + 1, tm)
            worksheet.write(row, col + 2, dict_tm[tm])
            row += 1
        print(" Итого ТС:", (c + 1))
        worksheet.write(row, col, "Итого ТС:")
        worksheet.write(row, col + 1, (c + 1))
        row += 1
    print("Всего групп:", response.json()["totalItemsCount"])
    print("Всего ТС:", len(dict_tm), "\n")
    worksheet.write(row, col, "Всего групп:")
    worksheet.write(row, col + 1, response.json()["totalItemsCount"])
    row += 1
    worksheet.write(row, col, "Всего ТС:")
    worksheet.write(row, col + 1, len(dict_tm))
    workbook.close()

    return


def search_TS(id_TS, eid_org):
    """
    Поиск элемента по ID
    :param eid_org: ID - сессии,
    :param id_TS: ID - транспортного средства
    :return:
    """
    params = {"id": id_TS, "flags": 1025}
    data = json.dumps(params, separators=(',', ':'))
    req_string = f"{URL}{comand_str_item}{data}&sid={eid_org}"
    print(req_string)
    response = requests.get(req_string)

    print("Список параметров элемента =", response.json(), "\n")
    print(len(response.json()["item"]))

    json_print_save("OUT\\OneID.json", response.json())

    return


def get_all_rounds(eid_org):
    params = {"spec": {"itemsType": "avl_unit", "propName": "sys_name", "propValueMask": "*",
                       "sortType": "sys_name"}, "force": 1, "flags": "0x00020001", "from": 0, "to": 0}
    data = json.dumps(params, separators=(',', ':'))
    req_string = f"{URL}{comand_str_items}{data}&sid={eid_org}"
    # print(req_string)
    response = requests.get(req_string)
