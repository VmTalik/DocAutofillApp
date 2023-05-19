import sqlite3, os

contracts_table = """CREATE TABLE IF NOT EXISTS contracts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        surname TEXT,
                        patronymic TEXT,
                        series TEXT,
                        number TEXT,
                        date TEXT,
                        contract BLOB
                        );"""


def convert_to_bin_data(file_name):
    """Функция преобразования данных в двоичный формат"""
    with open(file_name, 'rb') as file:
        blob_data = file.read()
    return blob_data


def insert_data(name, surname, patronymic, series, number, date, word_name):
    """Функция ввода данных в БД"""
    try:
        sqlite_connection = sqlite3.connect('contracts.db')
        cursor = sqlite_connection.cursor()
        cursor.execute(contracts_table)
        print("Подключен к SQLite")

        sqlite_insert_query = """INSERT INTO contracts
                                  (name, surname, patronymic, series, number, date, contract) VALUES (?, ?, ?, ?, ?, ?, ?)"""
        contract = convert_to_bin_data(word_name)
        data_tuple = (name, surname, patronymic, series, number, date, contract)
        cursor.execute(sqlite_insert_query, data_tuple)
        sqlite_connection.commit()
        print("Данные успешно внесены в БД")
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


query1 = """SELECT *
            FROM  contracts
            WHERE name = ? AND surname = ? AND patronymic = ?;"""
query2 = """SELECT *
            FROM  contracts
            WHERE date = ?;"""


def write_to_file(data, filename):
    # Преобразование двоичных данных в нужный формат
    with open(filename, 'wb') as file:
        file.write(data)
    print("Данный из blob сохранены в: ", filename, "\n")


def read_data(date, name='', surname='', patronymic=''):
    try:
        sqlite_connection = sqlite3.connect('contracts.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        if date:
            print('дата2')
            sql_fetch_query = query2
            cursor.execute(sql_fetch_query, (date,))
        else:
            sql_fetch_query = query1
            cursor.execute(sql_fetch_query, (name, surname, patronymic))
        record = cursor.fetchall()
        print(record)
        for row in record:
            name = row[1]
            surname = row[2]
            patronymic = row[3]
            series = row[4]
            number = row[5]
            date = row[6]
            contract = row[7]
            print("Сохранение файла\n")
            word_name = f'GNZ_result{series}{number}.docx'
            contract_path = os.path.join("selected_doс_db", word_name)
            write_to_file(contract, contract_path)
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
