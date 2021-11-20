import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import os.path
matplotlib.use('TkAgg')
plt.style.use('ggplot')


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
    
    def init_main(self):
        root["bg"] = "white"

        self.init_prices = np.arange(4) * 0 + 1
        self.init_nums = np.arange(4) * 0 + 1
        self.init_dollar = np.arange(4) * 0 + 1
        self.init_euro = np.arange(4) * 0 + 1
        self.init_add = np.arange(4) * 0 + 1

        self.init_size = 4
        self.init_names = np.array(['Бумага1', 'Бумага2', 'Бумага3', 'Бумага4'])
        self.init_currency = np.array(['Рубль', 'Рубль', 'Рубль', 'Рубль'])
        self.init_percents = np.array([25, 25, 25, 25])
        self.init_entry_prices = []
        self.init_entry_nums = []

        if os.path.exists('papers.csv'):
            papers = pd.read_csv('papers.csv')
            self.init_names = papers['Name'].values
            self.init_percents = papers['Percent'].values
            self.init_currency = papers['Currency'].values
            self.init_size = len(self.init_names)

        if os.path.exists('data.csv'):
            data = pd.read_csv('data.csv')
            self.init_prices = data['Price'].values
            self.init_nums = data['Num'].values
            self.init_dollar = data['Dollar'].values
            self.init_euro = data['Euro'].values
            self.init_add = data['Add'].values

        tk.Label(text='Цена', bg='white', justify='center').grid(row=0, column=1, pady=5, padx=5)
        tk.Label(text='Кол-во', bg='white', justify='center').grid(row=0, column=2, pady=5, padx=5)

        tk.Label(text='Долар ' + '( $ )', bg='white', justify='center').grid(row=self.init_size+1, column=0, pady=5,
                                                                             padx=5, sticky=tk.W)
        tk.Label(text='Евро ' + '( € )', bg='white', justify='center').grid(row=self.init_size + 2, column=0, pady=5,
                                                                           padx=5, sticky=tk.W)
        tk.Label(text='Добавить ' + '( ₽ )', bg='white', justify='center').grid(row=self.init_size+3, column=0, pady=5,
                                                                               padx=5, sticky=tk.W)

        self.entry_dollar_price = ttk.Entry(root, justify='center')
        self.entry_dollar_price.insert(0, self.init_dollar[0])
        self.entry_dollar_price.grid(row=self.init_size + 1, column=1, pady=5, padx=5)

        self.entry_euro_price = ttk.Entry(root, justify='center')
        self.entry_euro_price.insert(0, self.init_euro[0])
        self.entry_euro_price.grid(row=self.init_size + 2, column=1, pady=5, padx=5)

        self.entry_sum_buy = ttk.Entry(root, justify='center')
        self.entry_sum_buy.insert(0, self.init_add[0])
        self.entry_sum_buy.grid(row=self.init_size+3, column=1, pady=5, padx=5)

        for i in range(self.init_size):
            cur = ' '
            if self.init_currency[i] == 'Рубль':
                cur = '₽'
            if self.init_currency[i] == 'Доллар':
                cur = '$'
            if self.init_currency[i] == 'Евро':
                cur = '€'
            cur = ' ( ' + cur + ' )'
            tk.Label(text=self.init_names[i] + cur, bg='white').grid(row=i+1, column=0, sticky=tk.W, pady=5, padx=5)

            self.init_entry_prices.append(ttk.Entry(root, justify='center'))

            if i < len(self.init_prices):
                self.init_entry_prices[i].insert(0, self.init_prices[i])
            else:
                self.init_entry_prices[i].insert(0, 1)

            self.init_entry_prices[i].grid(row=i+1, column=1, sticky=tk.W, pady=5, padx=5)

            self.init_entry_nums.append(ttk.Entry(root, justify='center'))

            if i < len(self.init_nums):
                self.init_entry_nums[i].insert(0, self.init_nums[i])
            else:
                self.init_entry_nums[i].insert(0, 1)

            self.init_entry_nums[i].grid(row=i+1, column=2, sticky=tk.W, pady=5, padx=5)
        
        btn_portfel_now = tk.Button(root, text='Портфель сейчас', width=15, command=self.open_show_now)
        btn_portfel_now['bg'] = 'white'
        btn_portfel_now.grid(row=self.init_size+5, column=1, pady=5, padx=5)

        btn_to_buy = tk.Button(root, text='Докупить', width=15, command=self.open_to_buy)
        btn_to_buy['bg'] = 'white'
        btn_to_buy.grid(row=self.init_size+5, column=2, pady=5, padx=5)

        btn_save = tk.Button(root, text='Сохранить', width=15, command=self.save)
        btn_save['bg'] = 'white'
        btn_save.grid(row=self.init_size+4, column=1, pady=5, padx=5)

        btn_edit = tk.Button(root, text='Редактировать', width=15, command=self.open_edit)
        btn_edit['bg'] = 'white'
        btn_edit.grid(row=self.init_size+4, column=2, pady=5, padx=5)

    def how_many_buy(self):
        purpose_percent = self.init_percents / 100
        numbers = np.array([int(item.get()) for item in self.init_entry_nums])
        price = np.array([float(item.get()) for item in self.init_entry_prices])
        add = float(self.entry_sum_buy.get())
        sums = numbers * price
        sums *= self.convert_currency()

        total = sums.sum()
        new_total = total + add

        purpose_sums = purpose_percent * new_total

        diff = purpose_sums - sums
        diff /= self.convert_currency()

        to_buy = diff / price
        return np.round(to_buy)

    def open_show_now(self):
        numbers = np.array([int(item.get()) for item in self.init_entry_nums])
        prices = np.array([float(item.get()) for item in self.init_entry_prices])
        prices *= self.convert_currency()
        sums = numbers * prices
        total = sums.sum()
        percents = sums / total * 100
        
        labels = self.init_names
        sizes = percents

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        
        ax1.axis('equal')

        plt.show()

    def open_to_buy(self):
        to_buy = self.how_many_buy()
        to_buy = to_buy.astype(int)
        sum_to_buy = to_buy * np.array([float(item.get()) for item in self.init_entry_prices]) * self.convert_currency()
        money_to_add = float(self.entry_sum_buy.get())
        remains = round(money_to_add - sum_to_buy.sum(), 2)

        def add_labels(x, y):
            for i in range(len(x)):
                plt.text(i, y[i]/2, y[i], ha='center')
        x = self.init_names
        y = to_buy 
        y_list = y.tolist()
        for cur, ind in enumerate(self.init_currency):
            if cur == 'Доллар' or cur == 'Евро':
                y_list[ind] = y_list[ind] / 10
        plt.figure(figsize=(10, 5))
        plt.bar(x, y_list, color=['#e34930', '#318bbe', '#998fd6', '#777777', '#fbc25e'])
        add_labels(x, y_list)
        plt.title("Докупить бумаги. Остаток: " + str(remains) + " ₽")
        plt.show()

    def convert_currency(self):
        currency = []
        for cur in self.init_currency:
            if cur == 'Рубль':
                currency.append(1)
            if cur == 'Доллар':
                currency.append(float(self.entry_dollar_price.get()))
            if cur == 'Евро':
                currency.append(float(self.entry_euro_price.get()))
        currency = np.array(currency)
        return currency

    def open_edit(self):
        Edit()

    def refresh(self):
        length = len(self.init_entry_prices)-1
        while length+1:
            self.init_entry_prices[length].destroy()
            self.init_entry_nums[length].destroy()
            length -= 1
        self.init_entry_prices = []
        self.init_entry_nums = []

        for i in range(self.init_size):

            tk.Label(text=self.init_names[i], bg = 'white').grid(row=i+1, column=0, sticky=tk.W, pady=5, padx=5)

            self.init_entry_prices.append(ttk.Entry(root, justify='center'))
            self.init_entry_prices[i].grid(row=i+1, column=1, sticky=tk.W, pady=5, padx=5)

            self.init_entry_nums.append(ttk.Entry(root, justify='center'))
            self.init_entry_nums[i].grid(row=i+1, column=2, sticky=tk.W, pady=5, padx=5)

    def save(self):
        data = pd.DataFrame(columns=['Price', 'Num', 'Dollar', 'Euro', 'Add'])

        prices = [float(item.get()) for item in self.init_entry_prices]
        nums = [int(item.get()) for item in self.init_entry_nums]
        dollar = float(self.entry_dollar_price.get())
        euro = float(self.entry_euro_price.get())
        add = float(self.entry_sum_buy.get())

        data.loc[:, 'Price'] = prices
        data.loc[:, 'Num'] = nums
        data.loc[:, 'Dollar'] = dollar
        data.loc[:, 'Euro'] = euro
        data.loc[:, 'Add'] = add
        
        data.to_csv('data.csv', index=False)


class Edit(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()

    def init_child(self):
        self.title("Изменить бумаги")
        self.geometry("+570+180")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        self["bg"] = "white"

        self.list_entry_names = []
        self.list_entry_percents = []
        self.list_entry_currency = []
        init_size = 4

        self.list_names = ['Бумага1', 'Бумага2', 'Бумага3', 'Бумага4']
        self.list_percents = [0, 0, 0, 0]
        self.list_currency = ['Рубль', 'Рубль', 'Рубль', 'Рубль']

        if os.path.exists('papers.csv'):
            df = pd.read_csv('papers.csv')
            self.list_names = df['Name'].values
            self.list_percents = df['Percent'].values
            self.list_currency = df['Currency'].values
            init_size = len(self.list_percents)

        self.entery_num = ttk.Combobox(self, values=list(np.arange(15)+1), width=5, justify='center')
        self.entery_num.bind("<<ComboboxSelected>>", self.create_lines)
        self.entery_num.insert(0, init_size)
        self.entery_num.grid(row=0, column=0)

        tk.Label(self, text='Назвние', bg='white', justify='center').grid(row=0, column=1, pady=5, padx=5)
        tk.Label(self, text='Процент', bg='white', justify='center').grid(row=0, column=2, pady=5, padx=5)
        tk.Label(self, text='Валюта', bg='white', justify='center').grid(row=0, column=3, pady=5, padx=5)

        self.btn_save = tk.Button(self, text='Сохранить', width=15, command=self.save)
        self.btn_save['bg'] = 'white'
        self.btn_save.grid(row=int(self.entery_num.get())+2, column=2, pady=5, padx=5)

        self.create_lines(None)

    def create_lines(self, event):
        num = int(self.entery_num.get())

        if len(self.list_entry_names):
            length = len(self.list_entry_names)-1
            while length+1:
                self.list_entry_percents[length].destroy()
                self.list_entry_names[length].destroy()
                self.list_entry_currency[length].destroy()
                length -= 1
                
            self.list_entry_percents = []
            self.list_entry_names = []
            self.list_entry_currency = []

        for i in range(num):
            self.list_entry_names.append(ttk.Entry(self, justify='center'))
            if i < len(self.list_names):
                self.list_entry_names[i].insert(0, self.list_names[i])
            else:
                self.list_entry_names[i].insert(0, 'Бумага'+str(i))
            self.list_entry_names[i].grid(row=i + 1, column=1, sticky=tk.W, pady=5, padx=5)

            self.list_entry_percents.append(ttk.Entry(self, justify='center'))
            if i < len(self.list_percents):
                self.list_entry_percents[i].insert(0, self.list_percents[i])
            else:
                self.list_entry_percents[i].insert(0, 0)
            self.list_entry_percents[i].grid(row=i + 1, column=2, sticky=tk.W, pady=5, padx=5)

            self.list_entry_currency.append(ttk.Combobox(self, justify='center', values=['Рубль', 'Доллар', 'Евро']))
            if i < len(self.list_currency):
                self.list_entry_currency[i].insert(0, self.list_currency[i])
            else:
                self.list_entry_currency[i].insert(0, 'Рубль')
            self.list_entry_currency[i].grid(row=i + 1, column=3, sticky=tk.W, pady=5, padx=5)

        self.btn_save.destroy()
        self.btn_save = tk.Button(self, text='Сохранить', width=15, command=self.save)
        self.btn_save['bg'] = 'white'
        self.btn_save.grid(row=int(self.entery_num.get())+2, column=2, pady=5, padx=5)

    def save(self):
        df = pd.DataFrame(columns=['Name', 'Percent'])
        names = [item.get() for item in self.list_entry_names]
        percents = [item.get() for item in self.list_entry_percents]
        currency = [item.get() for item in self.list_entry_currency]
        df.loc[:, 'Name'] = names
        df.loc[:, 'Percent'] = percents
        df.loc[:, 'Currency'] = currency
        df.to_csv('papers.csv', index=False)
        self.destroy()
        root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.title("Инвестиционный Портфель")
    root.geometry("+570+180")
    root.resizable(False, False)
    root.mainloop()
