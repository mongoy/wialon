from datetime import datetime, date, time, timezone
import json
import sys

# скрытый ввод пароля
from getpass import getpass
# Импортируем библиотеку по работе с SMTP
import smtplib
# Добавляем необходимые подклассы - MIME-типы
from email.mime.multipart import MIMEMultipart      # Многокомпонентный объект
from email.mime.text import MIMEText                # Текст/HTML
from email.mime.image import MIMEImage
from token_org import *


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
    # text = json.dumps(obj, sort_keys=True, indent=4, ensure_ascii=False)
    # print("text =", text)
    with open(file_name, "w") as write_file:
        json.dump(obj, write_file, sort_keys=True, indent=4, ensure_ascii=False)

    # print(text)
    return


def send_email():
    """
    Отправка на e-mail
    :return:
    """
    addr_from = "a_antropov@mail.ru"  # Адресат
    addr_to = "antropov.adz@mail.ru"  # Получатель
    password = getpass()  # Пароль

    msg = MIMEMultipart()  # Создаем сообщение
    msg['From'] = addr_from  # Адресат
    msg['To'] = addr_to  # Получатель
    msg['Subject'] = 'Список транспортных средств'  # Тема сообщения

    body = "Список групп системы мониторинга с перечнем транспортных средств"
    msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст

    server = smtplib.SMTP('smtp.mail.ru', 25)  # Создаем объект SMTP
    server.set_debuglevel(True)  # Включаем режим отладки - если отчет не нужен, строку можно закомментировать
    server.starttls()  # Начинаем шифрованный обмен по TLS
    server.login(addr_from, password)  # Получаем доступ
    server.send_message(msg)  # Отправляем сообщение
    server.quit()  # Выходим

    return