import datetime
from eid_org import eid, logout
from list_TM import search_list_TS, search_TS, get_all_rounds, search_list_group_TS
from reports import search_reports, periodic_report, report
from export import export_to_xlsx
from add_moduls import send_email, set_period, report_to_excel
from proba import prb2


def send_sub():
    """
    Отправка почтового сообщения с почтового сервера MAIL.RU
    :return:
    """
    # files = ["file1_path",                                    # Список файлов, если вложений нет, то files=[]
    #          "file2_path",
    #          "dir1_path"]
    files = ["OUT\\List_group_TM.xlsx"]
    now = datetime.datetime.now()
    msg_subj = "Для Юдиной Анастасии. Тестовое письмо"
    msg_text = "Wialon. Список групп транспортных средств на " + str(now.strftime("%d-%m-%Y %H:%M")) + "\n Алексей"
    send_email(msg_subj, msg_text, files)
    return


if __name__ == "__main__":
    # Вход
    CONST_SID = eid()

    # 1 Список транспортных средств RAB
    # search_list_TS(CONST_SID)

    # 2 Поиск элемента по ID  RAB
    # search_TS(21369586, CONST_SID)

    # 3 Список отчётов RUB
    # search_reports(CONST_SID)

    # 4 Получение пробега  и данных по расходу топлива за период RUB
    # prb2(CONST_SID)
    periodic_report(CONST_SID)
    # report(CONST_SID)
    # set_period()
    # report_to_excel(1)

    # 5 Экспорт
    # export_to_xlsx(CONST_SID)

    # 6 Список групп транспортных средств RUB
    # search_list_group_TS(CONST_SID)

    # 7 Отправка на e-mail RUB
    # send_sub()

    # 8

    # Выход
    logout(CONST_SID)
