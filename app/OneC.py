import pyautogui as pg
import datetime
import time
import cv2
import openpyxl
import os
from .urls import *



class PgCustomFuncs:
    def __init__(self):
        pass

    def locate(self, x):
        return pg.locateCenterOnScreen(x, confidence=0.9)
    
    def wait_until_locate(self, x):
        D = self.locate(x)
        while D == None:
            D = self.locate(x)
        return D
    
    def wait_and_click(self, x):
        pg.leftClick(self.wait_until_locate(x))

    def scroll_and_click(self, x, scroll_speed):
        a = self.locate(x)
        while a == None:
            pg.scroll(scroll_speed)
            a = self.locate(x)
        pg.leftClick(a)

class OnecHelperFuncs(PgCustomFuncs):
    def __init__(self):
        pass 

    def enter_name_password_and_apply(self, mainN, PASS):

        self.wait_and_click(OPEN1C_URL+'SName_indicator.png')

        pg.press('down')
        pg.move(0, 25)

        self.scroll_and_click(mainN, -350)

        self.wait_and_click(OPEN1C_URL+'pass_indicator.png')
        pg.typewrite(PASS)

        self.wait_and_click(OPEN1C_URL+'onec_enter_apply.png')

        time.sleep(2)

        passs = self.locate(OPEN1C_URL+'wrongpass.png')
        if passs != None:
            self.wait_and_click(OPEN1C_URL+'wrongpassok.png')
    
    def open_1c(self, mainN, PASS):
        if self.locate(OPEN1C_URL+'onec_icon_opened.png') == None:

            self.wait_and_click(OPEN1C_URL+'onec_icon.png')

            self.wait_and_click(OPEN1C_URL+'onec_pred.png')

            self.enter_name_password_and_apply(mainN, PASS)
        else:
            if self.locate(OPEN1C_URL+'onec_ind.png') == None:

                self.wait_and_click(OPEN1C_URL+'onec_icon_opened.png')

    def open_skype(self):
        if self.locate(SKYPE_URL+'skype_icon_opened.png') == None:
            if self.locate(SKYPE_URL+'skype_icon_alert.png') != None:
                self.wait_and_click(SKYPE_URL+'skype_icon_alert.png')
            else:
                self.wait_and_click(SKYPE_URL+'skype_icon_closed.png')
        else:
            if self.locate(SKYPE_URL+'skype_ind.png') == None:
                self.wait_and_click(SKYPE_URL+'skype_icon_opened.png')

    def send_exchange_result(self, ex_res, tst=False):
        self.open_skype()

        if self.locate(SKYPE_URL+'chat_important.png') == None:
            self.wait_and_click(SKYPE_URL+'chat_important_alert.png')
        else:
            self.wait_and_click(SKYPE_URL+'chat_important.png')

        self.wait_and_click(SKYPE_URL+'skype_enter_message.png')

        # отправить результат обмена
        if tst == False:
            pg.typewrite(ex_res)
            pg.press('enter')

    def make_full_win(self):

        self.wait_until_locate(OPEN1C_URL+'onec_ind.png')

        while 1:
            if self.locate(OTHER_URL+'make_full_win.png') != None:
                self.wait_and_click(OTHER_URL+'make_full_win.png')
                break
            if self.locate(OTHER_URL+'make_small_win.png') != None:
                break
    
    def make_full_check(self):
        d = False
        while d == False:
            if self.locate(CHECKLIST_URL+'Checklist_make_small.png') != None:
                d = True 
                break
            if self.locate(CHECKLIST_URL+'Checklist_make_full.png') != None:
                self.wait_and_click(CHECKLIST_URL+'Checklist_make_full.png')
                d = True 
                break

    def make_full_reg(self):
        while 1:
            if self.locate(REGISTRATION_URL+'make_full_reg.png') != None:
                self.wait_and_click(REGISTRATION_URL+'make_full_reg.png')
                break
            if self.locate(REGISTRATION_URL+'make_small_reg.png') != None:
                break

    def close_office_lisense(self):
        D = self.locate(CHECKLIST_URL+'Office_close.png')
        while D == None:
            D = self.locate(CHECKLIST_URL+'Office_close.png')
            pg.move(10,10)
        pg.leftClick(D)

    def kpi(self, mainN, PASS):
        day = str(datetime.datetime.now().date())[8:10]
        mounth = str(datetime.datetime.now().date())[5:7]
        year = str(datetime.datetime.now().date())[0:4]

        self.open_1c(mainN, PASS)

        self.wait_and_click(CHECKLIST_URL+'Checklist_reports.png')
        self.wait_and_click(CHECKLIST_URL+'Checklist_kpi.png')

        if self.locate(CHECKLIST_URL+'Checklist_kpi_indicator.png') == None:
            self.wait_and_click(CHECKLIST_URL+'Checklist_from.png')
            pg.typewrite('01'+mounth+year)

            self.wait_and_click(CHECKLIST_URL+'Checklist_to.png')
            pg.typewrite(day+mounth+year)

            is_full = self.locate(CHECKLIST_URL+'make_full_kpi.png')
            if is_full != None:
                self.wait_and_click(CHECKLIST_URL+'make_full_kpi.png')

            self.wait_and_click(CHECKLIST_URL+'Checklist_kpi_apply.png')
    
class Onec(OnecHelperFuncs):

    def __init__(self) -> None:
        pass
    
    def registration(self, mainN, regN, PASS, tst=False):
        self.open_1c(mainN, PASS)

        self.make_full_win()

        self.wait_until_locate(OPEN1C_URL+'onec_ind.png')
        
        if self.locate(REGISTRATION_URL+'Reg_close.png') != None:
            self.wait_and_click(REGISTRATION_URL+'Reg_close.png')

        self.wait_and_click(REGISTRATION_URL+'Reg.png')

        self.make_full_reg()

        self.wait_and_click(REGISTRATION_URL+'Reg_indicator.png')

        pg.press('down')
        pg.move(0, 20)

        self.scroll_and_click(regN, -350)

        self.wait_and_click(REGISTRATION_URL+'Reg_pass_ind.png')
        pg.typewrite(PASS)

        self.wait_and_click(REGISTRATION_URL+'make_small_reg.png')

        if tst == True:
            self.wait_and_click(REGISTRATION_URL+'Reg_close.png')
        else:
            self.wait_and_click(REGISTRATION_URL+'Reg_apply_start.png')
            self.wait_and_click(REGISTRATION_URL+'Reg_apply_yes.png')
            self.wait_and_click(REGISTRATION_URL+'Reg_apply_ok.png')

    def exchange(self, mainN, PASS, tst=False):
        MANUAL = False

        self.open_1c(mainN, PASS)

        self.wait_and_click(EXCHANGE_URL+'exchange1.png')

        self.wait_and_click(EXCHANGE_URL+'exchange2.png')

        self.wait_until_locate(EXCHANGE_URL+'exchange_done.png')

        time.sleep(5)

        if self.locate(EXCHANGE_URL+'exchange_manual.png') != None:
            MANUAL = True

        if MANUAL == False:
            if pg.locateCenterOnScreen(EXCHANGE_URL+'exchange_failed.png', confidence=0.9) == None:
                ex1 = '+'
            else:
                ex1 = '-'
            if pg.locateCenterOnScreen(EXCHANGE_URL+'exchange_success.png', confidence=0.9) != None:
                ex2 = '+'
            else:
                ex2 = '-'

            self.wait_and_click(EXCHANGE_URL+'exchange_ok.png')
           
            self.wait_and_click(EXCHANGE_URL+'exchange_close.png')
            
            # self.wait_and_click(EXCHANGE_URL+'Alert_message_close.png')
            
            exchange_res = ex1+ex2

        else:
            self.wait_and_click(EXCHANGE_URL+'exchange_manual_yes.png')
            self.wait_and_click(EXCHANGE_URL+'exchange_manual_enter_pass.png')
            pg.typewrite(PASS)
            self.wait_and_click(EXCHANGE_URL+'exchange_manual_pass_apply.png')

            self.wait_until_locate(EXCHANGE_URL+'exchange_manual_done_ind.png')

            ex_close = self.locate(EXCHANGE_URL+'exchange_manual_close_alert.png')
            while ex_close != None:
                pg.leftClick(ex_close)
            exchange_res = '++'

        self.send_exchange_result(exchange_res, tst)

    def open_shift(self, mainN, shopN, PASS, tst=False):
        self.open_1c(mainN, PASS)

        self.wait_and_click(OPENSHIFT_URL+'sells.png')

        self.wait_and_click(OPENSHIFT_URL+'shift.png')

        self.wait_until_locate(OPENSHIFT_URL+'shifts_indicator.png')

        self.wait_and_click(OPENSHIFT_URL+'cashbox.png')

        cashbox = self.locate(shopN)
        while cashbox == None:
            pg.press('down')
            cashbox = self.locate(shopN)

        pg.leftClick(cashbox)

        # открыть смену
        if tst == False:
            self.wait_and_click(OPENSHIFT_URL+'open_shift_btn.png')

        # закрыть окно
        self.wait_and_click(OPENSHIFT_URL+'shift_close_window.png')

    def send_open_time(self, tst=False):
        time = str(datetime.datetime.now().time())[1:5]
        mins = time[-2:]
        time1 = time[:-2]
        if int(mins) > 50:
            mins = '50'
        else:
            mins = str(int(mins)-2)
        time = time1+mins

        self.open_skype()
        if self.locate(SKYPE_URL+'chat_time.png') == None:
            self.wait_and_click(SKYPE_URL+'chat_time_alert.png')
        else:
            self.wait_and_click(SKYPE_URL+'chat_time.png')

        self.wait_and_click(SKYPE_URL+'skype_enter_message.png')

        # отправить время
        if tst == False:
            pg.typewrite(time)
            pg.press('enter')

    def close_archiving(self):
        if self.locate(ARCHIVING_URL+'Archiving_icon_opened.png') != None:
            self.wait_and_click(ARCHIVING_URL+'Archiving_icon_opened.png')

            self.wait_until_locate(ARCHIVING_URL+'Archiving_done.png')

            self.wait_and_click(ARCHIVING_URL+'Archiving_close.png')

    def checklist(self,name,mainN,checkN,shop,PASS, tst=False):
        # Дата
        day = str(datetime.datetime.now().date())[8:10]
        mounth = str(datetime.datetime.now().date())[5:7]
        year = str(datetime.datetime.now().date())[0:4]
        data = day+'.'+mounth+'.'+year

        # Формируем отчет kpi
        self.kpi(mainN, PASS)

        self.wait_and_click(CHECKLIST_URL+'Checklist_kk_ind.png')
        # Проверяем есть ли у продавца показатели (None or not None) 
        does_worker_has_kpi  = self.locate(checkN)

        if does_worker_has_kpi != None:
            self.wait_and_click(checkN)

        else:
            self.wait_and_click(CHECKLIST_URL+'Checklist_shop_ind.png')

        pg.dragTo(self.locate(CHECKLIST_URL+'Checklist_avgCheck_ind.png'),button='left')

        pg.rightClick()
        self.wait_and_click(CHECKLIST_URL+'Checklist_copy.png')

        os.startfile(CHECKLIST_URL+'Kpi.xlsx', 'open')
        self.make_full_check()

        if shop in ['Домодедовская', 'Европейский']:
                self.close_office_lisense()
                pg.leftClick(500,500)

        self.wait_and_click(CHECKLIST_URL+'Checklist_all.png')
            
        self.wait_and_click(CHECKLIST_URL+'Checklist_delete.png')
                
        self.wait_and_click(CHECKLIST_URL+'Checklist_paste.png')
                
        self.wait_and_click(CHECKLIST_URL+'Checklist_kpi_ok.png')
                

        if shop == 'Крылатское':
            self.wait_and_click(CHECKLIST_URL+'Checklist_close.png')
        if shop in ['Домодедовская', 'Европейский']:
            self.wait_and_click(CHECKLIST_URL+'Checklist_close_dmd.png')

        self.wait_and_click(CHECKLIST_URL+'Checklist_save_sure.png')

        self.open_1c(mainN, PASS)

        self.wait_and_click(CHECKLIST_URL+'Checklist_kpi_close.png')

   
        wb = openpyxl.load_workbook(CHECKLIST_URL+"Kpi.xlsx")
        kpi = wb.active

        TOplan = kpi['H4'].value
        CHECKplan = kpi['J4'].value

        if day != '01':
            TO = kpi['E4'].value
            if does_worker_has_kpi != None:
                n = 1
                while kpi['B'+str(n)].value != name:
                    n += 1
                CHECKpersonal = kpi['K'+str(n)].value
            else:
                CHECKpersonal = '0'
            
        else:
            TO = '0'
            CHECKpersonal = '0'
        
        # Получив показатели по одному из случаев формируем и печатаем чеклист
        wb2 = openpyxl.load_workbook(
            CHECKLIST_URL+"DefChecklist.xlsx")
        checklist = wb2.active

        checklist['G3'].value = data
        checklist['C4'].value = shop
        checklist['C5'].value = name
        checklist['C40'].value = TOplan
        checklist['C42'].value = TO
        checklist['C43'].value = CHECKplan
        checklist['C45'].value = CHECKpersonal

        wb2.template = False

        wb2.save(CHECKLIST_URL+'DefChecklist.xlsx')

        os.startfile(CHECKLIST_URL+'DefChecklist.xlsx', 'open')
        self.make_full_check()
        if shop in ['Домодедовская', 'Европейский']:
            self.close_office_lisense()

        if shop == 'Крылатское':
            self.wait_and_click(CHECKLIST_URL+'Checklist_close.png')
        if shop in ['Домодедовская', 'Европейский']:
            self.wait_and_click(CHECKLIST_URL+'Checklist_close_dmd.png')
        
    
        if self.locate(CHECKLIST_URL+'Checklist_save_sure.png') != None:
            self.wait_and_click(
                CHECKLIST_URL+'Checklist_save_sure.png')
        
        os.startfile(CHECKLIST_URL+'DefChecklist.xlsx', 'print')