# Отчёты
import requests
import json
import datetime
from settings import *
from add_moduls import DataTime_to_sec, set_period, json_print_save, json_print, report_to_excel
from list_TM import search_list_TS, search_list_group_TS


def search_reports(eid_org):
    """
    Список отчётов пользователя
    :return:
    """
    params = {"spec": {"itemsType": "avl_resource", "propName": "reporttemplates", "propValueMask": "*",
                       "sortType": "reporttemplates"}, "force": 1, "flags": "0x00002001", "from": 0, "to": 0}
    data = json.dumps(params, separators=(',', ':'))
    req_string = f"{URL}{command_core_search_items}{data}&sid={eid_org}"
    # print(req_string)
    response = requests.get(req_string)
    # print("Отчёт =", response.json(), "\n")
    # print("Отчёты =", json_print(response.json()["items"]))
    json_print_save("OUT\\reports.json", response.json())
    return


def periodic_report(eid_org):
    """
    Получение пробега  и данных по расходу топлива ("reportTemplateId":
    ID 21345040 - "KGUP75"
    ТС "Камаз к678ст" ID 21369701 за прошедшие сутки
    :return: список поездок и остановок ТС по группам
    """
    # date_first, date_last = set_period()
    date_first, date_last = [1611068400, 1611241200]
    period = f"{datetime.datetime.fromtimestamp(date_first)}" \
             f" - {datetime.datetime.fromtimestamp(date_last)}"
    #
    # Получение перечня техники
    # Выгрузка списка транспортных средств
    dict_tm = search_list_TS(eid_org)
    # Выгрузка списка групп
    list_group = search_list_group_TS(eid_org, 0)
    # print("Список групп ТС =", json_print(list_group.json()["items"]), "\n")
    # Перебор списка групп и создание списка для формирования таблици
    table_list = [[f"Движение ТС в период: {period}"], ["Всего групп:", list_group.json()["totalItemsCount"]]]

    for group_TM in list_group.json()["items"]:
        print("Группа:", group_TM["nm"], group_TM["id"])
        print("  ТС:")
        table_list.append(["Группа:", group_TM["nm"]])

        for c, tm in enumerate(group_TM["u"]):
            # print("  ", tm, dict_tm[tm])
            if tm == 21369733:
                print(21369733)
            table_list.append(["  ТС:", tm, dict_tm[tm]])
            # поиск сведений по ТС
            params = {"reportResourceId": 21345040, "reportTemplateId": 1, "reportObjectId": tm,
                      "reportObjectSecId": 0, "interval": {"from": date_first, "to": date_last, "flags": 0}}
            data = json.dumps(params, separators=(',', ':'))
            req_string = f"{URL}{command_report_exec_report}{data}&sid={eid_org}"
            # print(req_string, "\n")
            response = requests.get(req_string)
            status = ""
            if len(response.json()["reportResult"]["tables"]) > 0:
                # Данные по ТС за период
                # Поездки и Стоянки

                for row in range(len(response.json()["reportResult"]["tables"])):

                    if response.json()["reportResult"]["tables"][row]["label"] == "Поездки":
                        table_list.append([response.json()["reportResult"]["tables"][row]["label"]])
                        table_list.append(list(response.json()["reportResult"]["tables"][row]["header"]))
                        table_list.append(list(response.json()["reportResult"]["tables"][row]["total"]))
                        # print(response.json()["reportResult"]["tables"][row]["header"][6],
                        #       "-",
                        #       response.json()["reportResult"]["tables"][row]["total"][6]
                        #       )

                else:
                    status = "Нет данных"
                    # print(status)
                    table_list.append([status])
            else:
                status = "Нет данных"
                # print(status)
                table_list.append([status])

    # в excel
    print("Запись в файл")
    # report_to_excel(table_list)

    return


def report(eid_org):
    """
    Получение пробега  и данных по расходу топлива ("reportTemplateId":
    ID 21345040 - "KGUP75"
    ТС "Камаз к678ст" ID 21369701 за прошедшие сутки
    :return:
    """
    # https://hst-api.wialon.com/wialon/ajax.html?svc=report/exec_report&params=%7B%22reportResourceId%22:21345040,
    # %22reportTemplateId%22:1,%22reportObjectId%22:21369733,%22reportObjectSecId%22:0,%22interval%22:%7B%22from%
    # 22:1613833200,%22to%22:1616166000,%22flags%22:0%7D%7D&sid=106c832cd1be8625f65ea3ffefc27478

    date_first, date_last = [1613833200, 1616166000]
    period = f"{datetime.datetime.fromtimestamp(date_first)}" \
             f" - {datetime.datetime.fromtimestamp(date_last)}"
    # поиск сведений по ТС
    params = {"reportResourceId": 21345040, "reportTemplateId": 1, "reportObjectId": 21369733,
              "reportObjectSecId": 0, "interval": {"from": date_first, "to": + date_last, "flags": 0x00}}
    data = json.dumps(params, separators=(',', ':'))
    req_string = f"{URL}{command_report_exec_report}{data}&sid={eid_org}"
    # # print(req_string, "\n")
    response = requests.get(req_string)
    print(response.json())
    print()
    # req_string1 = 'https://hst-api.wialon.com/wialon/ajax.html?svc=report/get_result_rows&params={"tzOffset":25200,' \
    #               '"lang":"ru","reportResourceId":21345040,"reportTemplateId":25,"reportObjectId":21369733,' \
    #               '"reportObjectSecId":0,"interval":{"from":0,"to":0,"flags":0}}' \
    #               '&ssid=106c832cd1be8625f65ea3ffefc27478'


    # req_string1 = 'https://hst-api.wialon.com/wialon/ajax.html?svc=report/get_result_rows&params={' \
    #               '"tableIndex": 0,' \
    #               '"indexFrom": 1,' \
    #               '"indexTo": 2' \
    #               '}' \
    #               '&sid=106c832cd1be8625f65ea3ffefc27478'
    # response1 = requests.get(req_string1)
    # print(response1.json())
    # print()
