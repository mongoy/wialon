from eid_org import eid, logout
from list_TM import search_list_TS, search_TS


# Вход
CONST_SID = eid()

# 1 Список транспортных средств RAB
# search_list_TS(CONST_SID)


# 2 Поиск элемента по ID  RAB
# search_TS(21369586, CONST_SID)


# Выход
logout(CONST_SID)