from datetime import datetime, date, time, timezone
import json


def DataTime_to_sec(year, month, date, hour, minutes, seconds):
    """
    Преобразование даты в формат UNIX
    :return: date_unix
    """
    dt = datetime(year, month, date, hour, minutes, seconds)
    # timestamp = dt.replace(tzinfo=timezone.utc).timestamp()  # с учётом текущего часового пояса
    timestamp = dt.replace().timestamp()
    date_unix = int(timestamp)
    return date_unix


def json_print(obj):
    """
    создёт отформатированную строку объекта Python JSON
    :param obj:
    :return: text - строка формата JSON
    """
    text = json.dumps(obj, sort_keys=True, indent=4, ensure_ascii=False)
    print(text)
    return


def json_print_save(file_name, obj):
    """
    создёт отформатированную строку объекта Python JSON сохраняет в json-файл
    :param file_name:
    :param name, obj:
    :return: text - строка формата JSON
    """
    text = json.dumps(obj, sort_keys=True, indent=4, ensure_ascii=False)
    # print("text =", text)
    with open(file_name, "w") as write_file:
        json.dump(obj, write_file, sort_keys=True, indent=4, ensure_ascii=False)

    # print(text)
    return
