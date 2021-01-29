from datetime import datetime, date, time, timezone
import json
import os
from settings_org import addr_from, addr_to


# скрытый ввод пароля
from getpass import getpass
# Импортируем библиотеку по работе с SMTP
import smtplib
# Добавляем необходимые подклассы - MIME-типы
import mimetypes                                          # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
from email import encoders                                # Импортируем энкодер
from email.mime.base import MIMEBase                      # Общий тип
from email.mime.text import MIMEText                      # Текст/HTML
from email.mime.image import MIMEImage                    # Изображения
from email.mime.audio import MIMEAudio                    # Аудио
from email.mime.multipart import MIMEMultipart            # Многокомпонентный объект


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


def processing_attachement(msg, files):
    """
    Функция по обработке списка, добавляемых к сообщению файлов
    :param msg:
    :param files:
    :return:
    """
    for f in files:
        if os.path.isfile(f):                               # Если файл существует
            attach_file(msg, f)                             # Добавляем файл к сообщению
        elif os.path.exists(f):                             # Если путь не файл и существует, значит - папка
            dir_files = os.listdir(f)                       # Получаем список файлов в папке
            for file in dir_files:                          # Перебираем все файлы и...
                attach_file(msg, f+"/"+file)                # ...добавляем каждый файл к сообщению

    return


def attach_file(msg, filepath):
    """
    Функция по добавлению конкретного файла к сообщению
    :param msg:
    :param filepath:
    :return:
    """
    filename = os.path.basename(filepath)                   # Получаем только имя файла
    ctype, encoding = mimetypes.guess_type(filepath)        # Определяем тип файла на основе его расширения
    if ctype is None or encoding is not None:               # Если тип файла не определяется
        ctype = 'application/octet-stream'                  # Будем использовать общий тип
    maintype, subtype = ctype.split('/', 1)                 # Получаем тип и подтип
    if maintype == 'text':                                  # Если текстовый файл
        with open(filepath) as fp:                          # Открываем файл для чтения
            file = MIMEText(fp.read(), _subtype=subtype)    # Используем тип MIMEText
            fp.close()                                      # После использования файл обязательно нужно закрыть
    elif maintype == 'image':                               # Если изображение
        with open(filepath, 'rb') as fp:
            file = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
    elif maintype == 'audio':                               # Если аудио
        with open(filepath, 'rb') as fp:
            file = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
    else:                                                   # Неизвестный тип файла
        with open(filepath, 'rb') as fp:
            file = MIMEBase(maintype, subtype)              # Используем общий MIME-тип
            file.set_payload(fp.read())                     # Добавляем содержимое общего типа (полезную нагрузку)
            fp.close()
            encoders.encode_base64(file)                    # Содержимое должно кодироваться как Base64
    file.add_header('Content-Disposition', 'attachment', filename=filename)  # Добавляем заголовки
    msg.attach(file)                                        # Присоединяем файл к сообщению


def send_email(msg_subj, msg_text, files):
    """
    Отправка на e-mail
    :param msg_subj:
    :param msg_text:
    :param files:
    :return:
    """
    # addr_from = input('Введите e-mail отправителя:')
    password = getpass(f'Введите пароль ({addr_from}):')  # Пароль
    # addr_to = input('Введите e-mail получателя:')

    msg = MIMEMultipart()  # Создаем сообщение
    msg['From'] = addr_from  # Адресат
    msg['To'] = addr_to  # Получатель
    msg['Subject'] = msg_subj  # Тема сообщения

    body = msg_text
    msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст
    # присоединение файла
    processing_attachement(msg, files)

    server = smtplib.SMTP('smtp.mail.ru', 25)  # Создаем объект SMTP для MAIL.RU
    # server.set_debuglevel(True)  # Включаем режим отладки - если отчет не нужен, строку можно закомментировать
    server.starttls()  # Начинаем шифрованный обмен по TLS
    server.login(addr_from, password)  # Получаем доступ
    server.send_message(msg)  # Отправляем сообщение
    server.quit()  # Выходим

    return
