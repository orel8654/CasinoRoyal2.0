import random
import time
from bs4 import BeautifulSoup
import requests
import tkinter as tk

class Interface:
    
    def __init__(self):
        self.window = tk.Tk()
        self.lable = tk.Label(text='Милости прошу, к нашему Казину!', fg='white', bg='black', width=50, height=20)
        self.button = tk.Button(text='Начать!', width=5, height=2, bg='white', fg='black')
        self.window.title('Casino Python')
        self.lable.pack()
        self.button.pack()
        self.window.mainloop()

    def change_lable(self):
        pass

    def change_button(self):
        pass

    def change_entry(self):
        pass


class Another: #testing class

    def __init__(self, name='Unknown', money=0, val='rub', sex='Unknown'):
        super().__init__(name=name, money=money, val=val)
        self.sex = sex
    
    def change_sex(self, sex):
        self.sex = sex

class CoursMoney:

    URL = 'https://www.sravni.ru/valjuty/'
    HEADERS = {
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15', 
        'accept':'*/*',
        }

    def __init__(self):
        html = requests.get(CoursMoney.URL, headers=CoursMoney.HEADERS).text
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find('span', class_='cb-page__table-cell--value').get_text(strip=True)
        items = items.replace('₽', '').strip()
        items = items.replace(',', '.')

        self.USD = float(items)
        # print(f'Получили USD = {self.USD}')

        html = requests.get(CoursMoney.URL, headers=CoursMoney.HEADERS).text
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find('span', text='EUR').find_next('span', class_='cb-page__table-cell--value').get_text(strip=True)
        items = items.replace('₽', '').strip()
        items = items.replace(',', '.')

        self.EUR = float(items)
        # print(f'Получили EUR = {self.EUR}')

    def retmoney(self, val):
        print(f'Возвращаем {val}')
        if val == 'usd':
            return self.USD
        elif val == 'eur':
            return self.EUR

class SavesName:

    def __init__(self):
        pass

    def file_write(self, name):
        with open('name.txt', 'a', newline='') as file:
            file.write(name + '\n')

class Casino:

    def __init__(self, name='Unknown', money=0, val='rub'):
        self.name = name
        self.purse = money
        self.val = val
        self.count = 0

    def change_name(self, name):
        self.name = name
        save = SavesName()
        save.file_write(self.name)

    def plus_money(self, money):
        self.purse += money

    def minus_money(self, money):
        if self.purse > money:
            self.purse -= money

    def conver_val(self, val='rub'):
        if val == 'rub':
            self.purse = self.purse
        elif val == 'usd':
            usd = CoursMoney().retmoney(val)
            self.purse = self.purse / usd
            self.val = 'usd'
        elif val == 'eur':
            eur = CoursMoney().retmoney(val)
            self.purse = self.purse / eur
            self.val = 'eur'

    def info(self):
        return self.name, round(self.purse, 2), self.val

    def rolling(self, money):
        num = random.randint(1, 5)
        print('Загадал число от 1 до 5. Сделай выбор!')
        player_choose = int(input())
        if num == player_choose:
            if self.count % 2 == 0:
                print('Excellent..')
                self.purse += money * 2
            else:
                print('Oops..')
                self.purse -= money
        else:
            print('Oops..')
            self.purse -= money


x = Casino()
print(x.info())
name_s = input('Введите имя: ')
x.change_name(name_s)
money_s = int(input('Сколько денег в rub, хотите внести?: '))
x.plus_money(money_s)
val_s = int(input('Нужна ли конвертация? 1 - Да, 2 - Нет: '))
if val_s == 1:
    val_s_s = input('Какая валюта? "usd" или "eur": ')
    x.conver_val(val_s_s)
print(x.info())
print('Приступим к игре!')
while True:
    bet = int(input('На какую сумму хотите сыграть?: '))
    x.rolling(bet)
    print(x.info())
