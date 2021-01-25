TOKEN = "4e0158d1795214dc3d698c34e160b9720EA5B713ED26EA81D907FD83716C751EDF7D4C90"  # токен 23.12.20 - 30 дней
URL = "https://hst-api.wialon.com/wialon/ajax.html?"
comand_str_token = "svc=token/login&params="  # вход
comand_str_items = "svc=core/search_items&params="  # поиск элементов
comand_str_item = "svc=core/search_item&params="  # поиск параметров элемента
comand_str_report = "svc=report/exec_report&params="  # отчет
comand_str_rep_data = "svc=report/get_result_rows&params="  # отчет + данные одноуровневый отчёт +
# дополнительный запрос "svc=report/get_result_subrows&params="
comand_str_rep_mdata = "svc=report/select_result_rows&params="  # отчет + данные многоуровневый
comand_str_map = "svc=report/get_result_map&params="  # карта
comand_str_export = "svc=report/export_result&params="  # экспорт отчёта
comand_str_out = "svc=core/logout&params={}&sid="  # выход
