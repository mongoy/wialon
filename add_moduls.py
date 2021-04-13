import datetime
import json
import os
import xlsxwriter
from settings_org import addr_from, addr_to

# скрытый ввод пароля
from getpass import getpass
# Импортируем библиотеку по работе с SMTP
import smtplib
# Добавляем необходимые подклассы - MIME-типы
import mimetypes  # Импорт класса для обработки неизвестных MIME-типов,
# базирующихся на расширении файла
from email import encoders  # Импортируем энкодер
from email.mime.base import MIMEBase  # Общий тип
from email.mime.text import MIMEText  # Текст/HTML
from email.mime.image import MIMEImage  # Изображения
from email.mime.audio import MIMEAudio  # Аудио
from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект


def DataTime_to_sec(dt):
    """
    Преобразование даты в формат UNIX
    :param dt: дата + время
    :return: дата + время в секундах
    """
    print("Дата и время", dt.strftime("%d-%m-%Y %H:%M"), "\n")
    date_unix = int(dt.timestamp())
    print(date_unix, "\n")
    return date_unix


def set_period():
    """
    Установка периода времени
    :return: дата начала и окончания периода
    """
    period_type = int(input("0 - произвольный, 1 - фиксированный:"))
    if period_type == 0:
        dtb = input("ВВедите начальную дату в формате 'ДДММГГГГ':")
        dt = datetime.datetime(int(dtb[4:]), int(dtb[2:4]), int(dtb[0:2]))
        date_first = DataTime_to_sec(dt)  # Дата начала
        period = dt.strftime("%d-%m-%Y %H:%M") + " - "
        dte = input("ВВедите конечную дату в формате 'ДДММГГГГ':")
        dt = datetime.datetime(int(dte[4:]), int(dte[2:4]), int(dte[0:2]))
        date_last = DataTime_to_sec(dt)  # Дата окончания
        period += dt.strftime("%d-%m-%Y %H:%M")

    else:
        current_date = datetime.datetime.today()
        dt = current_date.combine((current_date.date() - datetime.timedelta(days=1)), current_date.min.time())
        date_first = DataTime_to_sec(dt)  # Дата начала
        period = dt.strftime("%d-%m-%Y %H:%M") + " - "
        dt = current_date.combine(current_date.date(), current_date.min.time())  # сегодня 00:00:00
        date_last = DataTime_to_sec(dt)  # Дата окончания
        period += dt.strftime("%d-%m-%Y %H:%M")

    print(period)

    return date_first, date_last


def json_print(obj):
    """
    создёт отформатированную строку объекта Python JSON
    :param obj:
    :return: строка формата JSON
    """
    text = json.dumps(obj, sort_keys=True, indent=4, ensure_ascii=False)
    print(text, "\n")
    return


def report_to_excel(tb):
    """
    создёт excel отчёт за прошедшие сутки по объекту JSON
    :param table: список списков с даными для таблицы
    :return:
    """
    # tb = [['Движение ТС в период: 2021-01-20 00:00:00 - 2021-01-22 00:00:00'],
    #       ['Всего групп:', 18],
    #       ['Группа:', '? Требуют уточнения'],
    #       ['  ТС:', 21369587, 'Грейдер 0535ЕЕ(Газимурозаводский ДЭУч)'],
    #       ['Нет данных за период: 2021-01-20 00:00:00 - 2021-01-22 00:00:00'],
    #       ['  ТС:', 21369594, 'Грейдер 1562ЕС(Газимурозаводский ДЭУч)'],
    #       ['Нет данных за период: 2021-01-20 00:00:00 - 2021-01-22 00:00:00'],
    #       ['  ТС:', 21369641, 'Грейдер 7497ЕХ(Нерчинский ДЭУч)'],
    #       ['Нет данных за период: 2021-01-20 00:00:00 - 2021-01-22 00:00:00'],
    #       ['  ТС:', 21369672, 'Грейдер 8964 ЕК(Газимурозаводский ДЭУч)'],
    #       ['Нет данных за период: 2021-01-20 00:00:00 - 2021-01-22 00:00:00'],
    #       ['  ТС:', 21369673, 'Грейдер 9004ЕО(Газимурозаводский ДЭУч)'],
    #       ['Нет данных за период: 2021-01-20 00:00:00 - 2021-01-22 00:00:00'],
    #       ['  ТС:', 21369733, 'Трактор Т-150 2556ОЕ(Газимурозаводский ДЭУч)'],
    #       ['Стоянки'],
    #       ['№', 'Начало', 'Конец', 'Положение', 'Длительность'],
    #       ['', '2021-01-20 00:07:38', '2021-01-20 02:02:52', '', '1:55:14']]

    # Создайте рабочую книгу и добавьте рабочий лист.
    workbook = xlsxwriter.Workbook('REP\\report1.xlsx')
    worksheet = workbook.add_worksheet('Транспортные средства')
    # Оформление
    # заголовок таблицы
    cell_format_table = workbook.add_format()
    cell_format_table.set_bold(True)
    cell_format_table.set_font_size(14)
    cell_format_table.set_bg_color('#CCCCCC')
    # заголовок строки
    cell_format_row = workbook.add_format()
    cell_format_row.set_font_size(14)
    cell_format_row.set_border(2)

    # Начните с первой ячейки. Строки и столбцы индексируются нулем.
    row = 0
    col = 0

    # worksheet.write(row, col, table[0])
    # row += 1
    #
    print(len(tb))
    for row_table in range(len(tb)):
        # Формирование списка
        for cel_table in range(len(tb[row_table])):
            if row_table == 0:
                worksheet.set_row(row, cell_format=cell_format_table)
                worksheet.write(row, col, tb[row_table][cel_table])
                row += 1
            else:
                worksheet.set_row(row, cell_format=cell_format_row)
                worksheet.write(row, col, tb[row_table][cel_table])
            # print(tb[row_table][cel_table])
            col += 1
        col = 0
        row += 1
    workbook.close()
    return


def json_print_save(file_name, obj):
    """
    создёт отформатированную строку объекта Python JSON сохраняет в json-файл
    :param file_name: путь к файлу
    :param obj:
    :return:
    """
    with open(file_name, "w") as write_file:
        json.dump(obj, write_file, sort_keys=True, indent=4, ensure_ascii=False)

    return


def processing_attachement(msg, files):
    """
    Функция по обработке списка, добавляемых к сообщению файлов
    :param msg: почтовое сообщение
    :param files: путь к файлу(ам) вложения
    :return:
    """
    for f in files:
        if os.path.isfile(f):  # Если файл существует
            attach_file(msg, f)  # Добавляем файл к сообщению
        elif os.path.exists(f):  # Если путь не файл и существует, значит - папка
            dir_files = os.listdir(f)  # Получаем список файлов в папке
            for file in dir_files:  # Перебираем все файлы и...
                attach_file(msg, f + "/" + file)  # ...добавляем каждый файл к сообщению

    return


def attach_file(msg, filepath):
    """
    Функция по добавлению конкретного файла к сообщению
    :param msg: почтовое сообщение
    :param filepath: путь к файлу(ам) вложения
    :return:
    """
    filename = os.path.basename(filepath)  # Получаем только имя файла
    ctype, encoding = mimetypes.guess_type(filepath)  # Определяем тип файла на основе его расширения
    if ctype is None or encoding is not None:  # Если тип файла не определяется
        ctype = 'application/octet-stream'  # Будем использовать общий тип
    maintype, subtype = ctype.split('/', 1)  # Получаем тип и подтип
    if maintype == 'text':  # Если текстовый файл
        with open(filepath) as fp:  # Открываем файл для чтения
            file = MIMEText(fp.read(), _subtype=subtype)  # Используем тип MIMEText
            fp.close()  # После использования файл обязательно нужно закрыть
    elif maintype == 'image':  # Если изображение
        with open(filepath, 'rb') as fp:
            file = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
    elif maintype == 'audio':  # Если аудио
        with open(filepath, 'rb') as fp:
            file = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
    else:  # Неизвестный тип файла
        with open(filepath, 'rb') as fp:
            file = MIMEBase(maintype, subtype)  # Используем общий MIME-тип
            file.set_payload(fp.read())  # Добавляем содержимое общего типа (полезную нагрузку)
            fp.close()
            encoders.encode_base64(file)  # Содержимое должно кодироваться как Base64
    file.add_header('Content-Disposition', 'attachment', filename=filename)  # Добавляем заголовки
    msg.attach(file)  # Присоединяем файл к сообщению


def send_email(msg_subj, msg_text, files):
    """
    Отправка на e-mail
    :param msg_subj: тема сообщения
    :param msg_text: текст сообщения
    :param files: путь к файлу(ам) вложения
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
