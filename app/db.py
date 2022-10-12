import sqlite3


class Db:

    def __init__(self):
        pass

    def convert_to_binary_data(self, filename):
        with open(filename, 'rb') as file:
            blob_data = file.read()
        return blob_data

    def add_user_to_db(self, name, main, reg, check):
        try:
            self.autoDb = sqlite3.connect('AutoSQL.db')
            self.autoCur = self.autoDb.cursor()

            self.autoCur.execute(
                """CREATE TABLE IF NOT EXISTS namelist (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, mainN BLOB NOT NULL, regN BLOB NOT NULL, checkN BLOB NOT NULL) """)

            sqlite_insert_blob_query = """INSERT INTO namelist(name, mainN, regN, checkN) VALUES (?,?,?,?)"""

            mainN = self.convert_to_binary_data(self, main)
            regN = self.convert_to_binary_data(self, reg)
            checkN = self.convert_to_binary_data(self, check)

            data_tuple = (name, mainN, regN, checkN)

            self.autoCur.execute(sqlite_insert_blob_query, data_tuple)

            self.autoDb.commit()
            self.autoCur.close()

        except sqlite3.Error as error:
            print('Ошибка при работе с SQLite', error)

        finally:
            if self.autoDb:
                self.autoDb.close()

    def add_shop_to_db(self, shopname, shop):
        try:
            self.autoDb = sqlite3.connect('AutoSQL.db')
            self.autoCur = self.autoDb.cursor()

            self.autoCur.execute(
                """CREATE TABLE IF NOT EXISTS shoplist (id INTEGER PRIMARY KEY AUTOINCREMENT, shop TEXT NOT NULL, shopN BLOB NOT NULL)""")

            sqlite_insert_blob_query = """INSERT INTO shoplist(shop, shopN) VALUES (?,?)"""

            shopN = self.convert_to_binary_data(self, shop)

            data_tuple = (shopname, shopN)

            self.autoCur.execute(sqlite_insert_blob_query, data_tuple)

            self.autoDb.commit()
            self.autoCur.close()

        except sqlite3.Error as error:
            print("ERROR", error)

        finally:
            if self.autoDb:
                self.autoDb.close()

    def get_names_and_shops_for_combobox(self):
        try:
            self.autoDb = sqlite3.connect('AutoSQL.db')
            self.autoCur = self.autoDb.cursor()

            self.autoCur.execute("SELECT name FROM namelist")
            names = self.autoCur.fetchall()

            self.autoCur.execute("SELECT shop FROM shoplist")
            shops = self.autoCur.fetchall()

            self.autoDb.commit()
            self.autoCur.close()
        except sqlite3.Error as error:
            print("ERROR", error)

        finally:
            if self.autoDb:
                self.autoDb.close()

            namelist = []
            for i in names:
                for j in i:
                    namelist.append(j)
            shoplist = []
            for k in shops:
                for b in k:
                    shoplist.append(k)

            return namelist, shoplist

    def binary_to_file(self, data, filename):
        with open(filename, 'wb') as file:
            file.write(data)

    def get_all_for_open(self, nameNum, shopNum):

        try:
            self.autoDb = sqlite3.connect('AutoSQL.db')
            self.autoCur = self.autoDb.cursor()

            # Получаем данный сотруда по id
            sql_fetch_name_query = f"""SELECT * FROM namelist WHERE id={nameNum}"""

            self.autoCur.execute(sql_fetch_name_query)

            record = self.autoCur.fetchall()

            for row in record:
                name = row[1]
                mainN_binary = row[2]
                regN_binary = row[3]
                checkN_binary = row[4]

            # Указываю пути к временным скриншотам имени
            mainN = 'mainN.png'

            regN = 'regN.png'

            checkN = 'checkN.png'

            # Преобразуем binary данные и записываем во временные файлы
            self.binary_to_file(self, mainN_binary, mainN)
            self.binary_to_file(self, regN_binary, regN)
            self.binary_to_file(self, checkN_binary, checkN)

            # Делаем все тоже самое для магазина
            sql_fetch_shop_query = f"""SELECT * FROM shoplist WHERE id={shopNum}"""

            self.autoCur.execute(sql_fetch_shop_query)

            record_shop = self.autoCur.fetchall()

            for row_shop in record_shop:
                shop = row_shop[1]
                shopN_binary = row_shop[2]

            shopN = 'shopN.png'

            self.binary_to_file(self, shopN_binary, shopN)

            self.autoDb.commit()
            self.autoCur.close()

        except sqlite3.Error as error:
            print("ERROR", error)

        finally:
            if self.autoDb:
                self.autoDb.close()
            return name, mainN, regN, checkN, shop, shopN
