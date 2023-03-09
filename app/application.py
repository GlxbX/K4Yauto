import tkinter as tk
from tkinter import Menu, ttk
from tkinter import filedialog as fd
import pyautogui as pg
import os
import cv2
from .db import Db
from .OneC import Onec


pg.PAUSE = 0.2

class Application(tk.Tk, Onec):
    # Конструктор
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('K4Y')

        self.resizable(False, False)
        self.attributes('-alpha', 1)
        self.set_ui()

    # Общие функции
    def clear_win(self):
        for i in self.winfo_children():
            i.destroy()

    def set_ui_menu(self):
        menu_bar = Menu(self)

        admin_menu = Menu(menu_bar, tearoff=0)
        admin_menu.add_command(label="Добавить сотрудника",
                               command=lambda: self.admin_pass('add_user'))
        admin_menu.add_command(label="Добавить магазин",
                               command=lambda: self.admin_pass('add_shop'))

        menu_bar.add_cascade(label="Открытие", command=self.set_ui)
        menu_bar.add_cascade(label="Админ", menu=admin_menu)

        self.configure(menu=menu_bar)

    # Админка
    # Вспомогательные функции
    def open_file(self, x):
        filename = fd.askopenfilename()
        x.insert(tk.END, filename)

    def add_user(self):
        name = self.usernameEntry.get()
        mainN = self.blah.get()
        regN = self.blah2.get()
        checkN = self.blah3.get()
        Db.add_user_to_db(Db, name, mainN, regN, checkN)

    def add_shop(self):
        shopname = self.shopnameEntry.get()
        shop = self.blahS.get()
        Db.add_shop_to_db(Db, shopname, shop)

    def is_admin(self, pswrd, action):
        PASSWORD = '1703'
        if pswrd == PASSWORD:
            if action == 'add_user':
                self.set_ui_admin_add_user()
            if action == 'add_shop':
                self.set_ui_admin_add_shop()
        else:
            self.wrondAdminPassLabel = ttk.Label(
                self.adminPassframe, text='Неверный пароль')
            self.wrondAdminPassLabel.pack(fill=tk.BOTH)

    def admin_pass(self, action):
        self.clear_win()
        self.geometry('400x200')

        # Меню
        menu_bar = Menu(self)

        admin_menu = Menu(menu_bar, tearoff=0)
        admin_menu.add_command(label="Добавить сотрудника",
                               command=lambda: self.admin_pass('add_user'))
        admin_menu.add_command(label="Добавить магазин",
                               command=lambda: self.admin_pass('add_shop'))

        menu_bar.add_cascade(label="Открытие", command=self.set_ui)
        menu_bar.add_cascade(label="Админ", menu=admin_menu)

        self.configure(menu=menu_bar)

        # Ввод пароля
        self.adminPassframe = ttk.Frame(self, padding=10)
        self.adminPassframe.pack(fill=tk.X)

        self.adminPasslabel = ttk.Label(
            self.adminPassframe, text='Для доступа необходимо ввести пароль администратора')
        self.adminPasslabel.pack(fill=tk.BOTH)

        self.pswr = ttk.Entry(self.adminPassframe, show='*')
        self.pswr.pack(side=tk.LEFT, fill=tk.X)

        self.adminPassbtn = ttk.Button(
            self.adminPassframe, text="Войти", command=lambda: self.is_admin(self.pswr.get(), action))
        self.adminPassbtn.pack(side=tk.RIGHT)

    # Интерфейс добавить сотрудника
    def set_ui_admin_add_user(self):
        # Очистить окно
        self.clear_win()
        self.geometry('400x365')

        # Меню
        self.set_ui_menu()

        # Ввод имени
        self.userFrame = ttk.Frame(self, padding=10)
        self.userFrame.pack(fill=tk.BOTH)

        self.userLabel = ttk.Label(self.userFrame, text='ФИО Сотрудника')
        self.userLabel.pack(fill=tk.X)

        self.usernameEntry = ttk.Entry(self.userFrame)
        self.usernameEntry.pack(fill=tk.X)

        # Выбор скриншотов
        self.bigFrame = ttk.Frame(
            self, padding=10, borderwidth=1, relief=tk.SOLID)
        self.bigFrame.pack(fill=tk.BOTH)

        self.screenshotLabel = ttk.Label(
            self.bigFrame, text='Добавление скриншотов ФИО')
        self.screenshotLabel.pack(side=tk.TOP)

        # Имя при открытии 1с
        self.main_screenshot_frame = ttk.Frame(self.bigFrame, padding=10)
        self.main_screenshot_frame.pack(fill=tk.X)

        self.mainN_label = ttk.Label(
            self.main_screenshot_frame, text='Выбор ФИО при открытии 1с')
        self.mainN_label.pack(fill=tk.BOTH)

        self.blah = ttk.Entry(self.main_screenshot_frame)
        self.blah.pack(side=tk.LEFT, fill=tk.X)

        self.choose_mainN_btn = ttk.Button(
            self.main_screenshot_frame, text="Выбрать", command=lambda: self.open_file(self.blah))
        self.choose_mainN_btn.pack(side=tk.RIGHT)

        # Имя в регистрации
        self.reg_screenshot_frame = ttk.Frame(self.bigFrame, padding=10)
        self.reg_screenshot_frame.pack(fill=tk.X)

        self.regN_label = ttk.Label(
            self.reg_screenshot_frame, text='Выбор ФИО в регистрации')
        self.regN_label.pack(fill=tk.BOTH)

        self.blah2 = ttk.Entry(self.reg_screenshot_frame)
        self.blah2.pack(side=tk.LEFT, fill=tk.X)

        self.choose_regN_btn = ttk.Button(
            self.reg_screenshot_frame, text="Выбрать", command=lambda: self.open_file(self.blah2))
        self.choose_regN_btn.pack(side=tk.RIGHT)

        # Имя в отчете KPI
        self.check_screenshot_frame = ttk.Frame(self.bigFrame, padding=10)
        self.check_screenshot_frame.pack(fill=tk.X)

        self.checkN_label = ttk.Label(
            self.check_screenshot_frame, text='Выбор ФИО в расчете KPI')
        self.checkN_label.pack(fill=tk.BOTH)

        self.blah3 = ttk.Entry(self.check_screenshot_frame)
        self.blah3.pack(side=tk.LEFT, fill=tk.X)

        self.choose_checkN_btn = ttk.Button(
            self.check_screenshot_frame, text="Выбрать", command=lambda: self.open_file(self.blah3))
        self.choose_checkN_btn.pack(side=tk.RIGHT)

        # Кнопка добавить сотрудника
        self.add_user_btn_frame = ttk.Frame(self, padding=10)
        self.add_user_btn_frame.pack(fill=tk.BOTH)

        self.add_user_btn = ttk.Button(
            self.add_user_btn_frame, text='Добавить сотрудника', command=self.add_user)
        self.add_user_btn.pack(side=tk.TOP)

    # Интерфейс добавить магазин
    def set_ui_admin_add_shop(self):
        self.clear_win()
        self.geometry('400x195')

        # Меню
        self.set_ui_menu()

        # Ввод имени магазина
        self.shopnameFrame = ttk.Frame(self, padding=10)
        self.shopnameFrame.pack(fill=tk.BOTH)

        self.shopnameLabel = ttk.Label(
            self.shopnameFrame, text='Название магазина')
        self.shopnameLabel.pack(fill=tk.X)

        self.shopnameEntry = ttk.Entry(self.shopnameFrame)
        self.shopnameEntry.pack(fill=tk.X)

        # Выбор скриншота
        self.onlyFrame = ttk.Frame(
            self, padding=10, borderwidth=1, relief=tk.SOLID)
        self.onlyFrame.pack(fill=tk.BOTH)

        self.shopN_label = ttk.Label(
            self.onlyFrame, text='Выберите название кассы магазина')
        self.shopN_label.pack(fill=tk.BOTH)

        self.blahS = ttk.Entry(self.onlyFrame)
        self.blahS.pack(side=tk.LEFT, fill=tk.X)

        self.choose_shopN_btn = ttk.Button(
            self.onlyFrame, text="Выбрать", command=lambda: self.open_file(self.blahS))
        self.choose_shopN_btn.pack(side=tk.RIGHT)

        # Кнопка добавить магазин
        self.add_shop_btn_frame = ttk.Frame(self, padding=10)
        self.add_shop_btn_frame.pack(fill=tk.BOTH)

        self.add_shop_btn = ttk.Button(
            self.add_shop_btn_frame, text='Добавить магазин', command=self.add_shop)
        self.add_shop_btn.pack(side=tk.TOP)

    # Пользователь
    # Визуальное оформление
    def set_ui(self):
        self.clear_win()

        self.geometry('400x400')

        # Меню
        self.set_ui_menu()

        # FOR COMBOBOXES
        namelist, shoplist = Db.get_names_and_shops_for_combobox(Db)

        # Магазин
        self.shopFrame = ttk.Frame(self, padding=10)
        self.shopFrame.pack(fill=tk.BOTH)

        self.shopLabel = ttk.Label(
            self.shopFrame, text='Магазин')
        self.shopLabel.pack(fill=tk.X)

        self.shopCombobox = ttk.Combobox(
            self.shopFrame, values=shoplist, state='readonly')
        self.shopCombobox.current(0)
        self.shopCombobox.pack(fill=tk.X)

        # Сотрудник
        self.nameFrame = ttk.Frame(self, padding=10)
        self.nameFrame.pack(fill=tk.BOTH)

        self.nameLabel = ttk.Label(self.nameFrame, text='Сотрудник')
        self.nameLabel.pack(fill=tk.X)

        self.nameCombobox = ttk.Combobox(
            self.nameFrame, values=namelist, state='readonly')
        self.nameCombobox.current(0)
        self.nameCombobox.pack(fill=tk.X)

        # Пароль
        self.passFrame = ttk.Frame(self, padding=10)
        self.passFrame.pack(fill=tk.BOTH)

        self.passLabel = ttk.Label(self.passFrame, text='Пароль')
        self.passLabel.pack(fill=tk.X)

        self.passEntry = ttk.Entry(self.passFrame, show='*')
        self.passEntry.pack(fill=tk.X)

        #Options
        self.var1 = tk.IntVar()
        self.var1.set(1)

        self.var2 = tk.IntVar()
        self.var2.set(1)

        self.var3 = tk.IntVar()
        self.var3.set(1)

        self.var4 = tk.IntVar()
        self.var4.set(1)
        
        self.var5 = tk.IntVar()
        self.var5.set(1)

        self.optionsFrame = ttk.Frame(self, padding=10)
        self.optionsFrame.pack(fill=tk.BOTH)

        self.optionsLabel = ttk.Label(self.optionsFrame, text='Опции')
        self.optionsLabel.pack(fill=tk.X)

        self.optionsCheckbutton1 = ttk.Checkbutton(self.optionsFrame, text='Время открытия', variable = self.var1)
        self.optionsCheckbutton1.pack(fill=tk.X)

        self.optionsCheckbutton2 = ttk.Checkbutton(self.optionsFrame, text='Регистрация', variable = self.var2)
        self.optionsCheckbutton2.pack(fill=tk.X)

        self.optionsCheckbutton3 = ttk.Checkbutton(self.optionsFrame, text='Кассовая смена', variable = self.var3)
        self.optionsCheckbutton3.pack(fill=tk.X)

        self.optionsCheckbutton4 = ttk.Checkbutton(self.optionsFrame, text='Обмен данными', variable = self.var4)
        self.optionsCheckbutton4.pack(fill=tk.X)

        self.optionsCheckbutton5 = ttk.Checkbutton(self.optionsFrame, text='Карта дня', variable = self.var5)
        self.optionsCheckbutton5.pack(fill=tk.X)

        # Кнопка Открыть
        self.openFrame = ttk.Frame(self, padding=10)
        self.openFrame.pack(fill=tk.BOTH)

        self.openBtn = ttk.Button(
            self.openFrame, text='ОТКРЫТЬ СМЕНУ', command=self.open)
        self.openBtn.pack(fill=tk.X)

        #Чекбар тест режима
        self.var6 = tk.IntVar()
        self.var6.set(0)

        self.testFrame = ttk.Frame(self, padding=5)
        self.testFrame.pack(fill=tk.BOTH)

        self.testCheckbutton1 = ttk.Checkbutton(self.testFrame, text='Тестовый режим', variable = self.var6)
        self.testCheckbutton1.pack(fill=tk.X)

    def get_NAME_and_SHOP(self):
        nameNum = self.nameCombobox.current() + 1
        shopNum = self.shopCombobox.current() + 1
        name, mainN, regN, checkN, shop, shopN = Db.get_all_for_open(Db,
                                                                     nameNum, shopNum)

        return name, mainN, regN, checkN, shop, shopN

    def open_funcs(self, name, mainN, regN, checkN, shop, shopN, PASS, tst):
        if self.var1.get():
            self.send_open_time(tst)

        self.close_archiving()

        if self.var2.get():
            self.registration(mainN, regN, PASS, tst)

        if self.var3.get():
            self.open_shift(mainN, shopN, PASS, tst)

        if self.var4.get():
            self.exchange(mainN, PASS, tst)

        if self.var5.get():
            self.checklist(name, mainN, checkN, shop, PASS, tst)

    def open(self):
        tst = self.var6.get()
     
        PASS = self.passEntry.get()
        if len(PASS) == 4:
            name, mainN, regN, checkN, shop, shopN = self.get_NAME_and_SHOP()

            self.open_funcs(name, mainN, regN, checkN,
                            shop, shopN, PASS, tst)
            os.remove(mainN)
            os.remove(regN)
            os.remove(checkN)
            os.remove(shopN)


