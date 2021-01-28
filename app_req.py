from eid_org import eid, logout
from list_TM import search_list_TS, search_TS, get_all_rounds, search_list_group_TS
from reports import search_reports, report
from export import export_to_xlsx
from proba import prb1
from add_moduls import send_email


# Вход
CONST_SID = eid()

# 1 Список транспортных средств RAB
# search_list_TS(CONST_SID)

# 2 Поиск элемента по ID  RAB
# search_TS(21369586, CONST_SID)

# 3 Список отчётов RUB
# search_reports(CONST_SID)

# 4 Получение пробега  и данных по расходу топлива за период RUB
# report(CONST_SID)

# 5 Экспорт
# export_to_xlsx(CONST_SID)

# 6 Список групп транспортных средств RUB
# search_list_group_TS(CONST_SID)

# 7 Отправка на e-mail
send_email()

# Выход
logout(CONST_SID)
