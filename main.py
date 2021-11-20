import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
plt.style.use('ggplot')
import pandas as pd
import os.path


class Main(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        self.init_main()
    
    def init_main(self):
        root["bg"] = "white"

        self.init_prices = np.arange(4) * 0 + 1
        self.init_nums = np.arange(4) * 0 + 1
        self.init_dolar = np.arange(4) * 0 + 1
        self.init_add = np.arange(4) * 0 + 1

        self.init_size = 4
        self.init_names = np.array(['NASDAQ', 'Games', 'Gold', 'Tips'])
        self.init_percents = np.array([25, 25, 25, 15])
        self.init_entry_prices = []
        self.init_entry_nums = []


        if os.path.exists('papers.csv'):
            papers = pd.read_csv('papers.csv')
            self.init_names = papers['Name'].values
            self.init_percents = papers['Precent'].values
            self.init_size = len(self.init_names)

        if os.path.exists('data.csv'):
            data = pd.read_csv('data.csv')
            self.init_prices = data['Price'].values
            self.init_nums = data['Num'].values
            self.init_dolar = data['Dolar'].values
            self.init_add = data['Add'].values

        tk.Label(text='Цена', bg = 'white', justify='center').grid(row=0, column=1, pady=5, padx=5)
        tk.Label(text='Кол-во', bg = 'white', justify='center').grid(row=0, column=2, pady=5, padx=5)

        tk.Label(text='Долар', bg = 'white', justify='center').grid(row=self.init_size+1, column=0, pady=5, padx=5, sticky=tk.W)
        tk.Label(text='Добавить', bg = 'white', justify='center').grid(row=self.init_size+2, column=0, pady=5, padx=5, sticky=tk.W)

        self.entry_dolar_price = ttk.Entry(root, justify='center')
        self.entry_dolar_price.insert(0, self.init_dolar[0])
        self.entry_dolar_price.grid(row=self.init_size+1, column=1, pady=5, padx=5)

        self.entry_sum_buy = ttk.Entry(root, justify='center')
        self.entry_sum_buy.insert(0, self.init_add[0])
        self.entry_sum_buy.grid(row=self.init_size+2, column=1, pady=5, padx=5)

        #print(self.init_size, self.init_entry_prices, self.init_prices)

        for i in range(self.init_size):

            tk.Label(text=self.init_names[i], bg = 'white').grid(row=i+1, column=0, sticky=tk.W, pady=5, padx=5)

            self.init_entry_prices.append(ttk.Entry(root, justify='center'))

            if i < len(self.init_prices):
                self.init_entry_prices[i].insert(0, self.init_prices[i])
            else:
                self.init_entry_prices[i].insert(0, 1)

            #self.init_entry_prices[i].insert(0, self.init_prices[i])
            self.init_entry_prices[i].grid(row=i+1, column=1, sticky=tk.W, pady=5, padx=5)

            self.init_entry_nums.append(ttk.Entry(root, justify='center'))

            if i < len(self.init_nums):
                self.init_entry_nums[i].insert(0, self.init_nums[i])
            else:
                self.init_entry_nums[i].insert(0, 1)

            #self.init_entry_nums[i].insert(0, self.init_nums[i])
            self.init_entry_nums[i].grid(row=i+1, column=2, sticky=tk.W, pady=5, padx=5)
        
        btn_portfel_now = tk.Button(root, text='Портфель сейчас', width=15, command=self.open_show_now)
        btn_portfel_now['bg'] = 'white'
        btn_portfel_now.grid(row=self.init_size+4, column=1, pady=5, padx=5)

        btn_to_buy = tk.Button(root, text='Докупить', width=15, command=self.open_to_buy)
        btn_to_buy['bg'] = 'white'
        btn_to_buy.grid(row=self.init_size+4, column=2, pady=5, padx=5)

        btn_save = tk.Button(root, text='Сохранить', width=15, command=self.save)
        btn_save['bg'] = 'white'
        btn_save.grid(row=self.init_size+3, column=1, pady=5, padx=5)

        btn_edit = tk.Button(root, text='Редактировать', width=15, command=self.open_edit)
        btn_edit['bg'] = 'white'
        btn_edit.grid(row=self.init_size+3, column=2, pady=5, padx=5)

        #btn_refresh = tk.Button(root, text='Обновить', width=15, command=self.refresh)
        #btn_refresh['bg'] = 'white'
        #btn_refresh.grid(row=self.init_size+2, column=2, pady=5, padx=5)


    def how_many_buy(self):
        porpose_precent = self.init_percents / 100
        numbers = np.array([int(item.get()) for item in self.init_entry_nums])
        price = np.array([float(item.get()) for item in self.init_entry_prices])
        dolar = float(self.entry_dolar_price.get())
        add = float(self.entry_sum_buy.get())

        sums = numbers * price
        sums[0] *= dolar

        total = sums.sum()
        new_total = total + add

        purpose_sums = porpose_precent * new_total

        diff = purpose_sums - sums
        diff[0] /= dolar

        to_buy = diff / price
        #print(to_buy, np.round(to_buy))
        return np.round(to_buy)



    def open_show_now(self):
        self.numbers_ = np.array([int(item.get()) for item in self.init_entry_nums])
        self.prices_ = np.array([float(item.get()) for item in self.init_entry_prices])

        prices = self.prices_.copy()
        dolar = float(self.entry_dolar_price.get())
        prices[0] *= dolar
        sums = self.numbers_ * prices
        total = sums.sum()
        precents = sums / total * 100
        
        labels = self.init_names
        sizes = precents

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        
        ax1.axis('equal')

        plt.show()


    def open_to_buy(self):
        to_buy = self.how_many_buy()
        to_buy = to_buy.astype(int)
        def addlabels(x,y):
            for i in range(len(x)):
                plt.text(i, y[i]/2, y[i], ha = 'center')
        x = self.init_names
        y = to_buy 
        y_list = y.tolist()
        y_list[0] = y_list[0] / 10
        plt.figure(figsize = (10, 5))
        plt.bar(x, y_list, color = ['#e34930','#318bbe', '#998fd6', '#777777', '#fbc25e'])
        addlabels(x, y_list)
        plt.title("Докупить бумаги")
        plt.show()

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
        data = pd.DataFrame(columns=['Price', 'Num', 'Dolar', 'Add'])

        prices = [float(item.get()) for item in self.init_entry_prices]
        nums = [int(item.get()) for item in self.init_entry_nums]
        dolar = float(self.entry_dolar_price.get())
        add = float(self.entry_sum_buy.get())

        data.loc[:, 'Price'] = prices
        data.loc[:, 'Num'] = nums
        data.loc[:, 'Dolar'] = dolar
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
        self.list_entry_precents = []
        init_size = 4

        self.list_names = ['Бумага', 'Бумага', 'Бумага', 'Бумага']
        self.list_precents = [0, 0, 0, 0]

        if os.path.exists('papers.csv'):
            df = pd.read_csv('papers.csv')
            self.list_names = df['Name'].values
            self.list_precents = df['Precent'].values
            init_size = len(self.list_precents)

        self.entery_num = ttk.Combobox(self, values=list(np.arange(15)+1), width=5, justify='center')
        self.entery_num.bind("<<ComboboxSelected>>", self.create_lines)
        self.entery_num.insert(0, init_size)
        self.entery_num.grid(row=0, column=0)

        tk.Label(self, text='Назвние', bg='white', justify='center').grid(row=0, column=1, pady=5, padx=5)
        tk.Label(self, text='Процент', bg='white', justify='center').grid(row=0, column=2, pady=5, padx=5)

        self.btn_save = tk.Button(self, text='Сохранить', width=15, command=self.save)
        self.btn_save['bg'] = 'white'
        self.btn_save.grid(row=int(self.entery_num.get())+2, column=2, pady=5, padx=5)

        self.create_lines(None)

    def create_lines(self, event):
        num = int(self.entery_num.get())

        if len(self.list_entry_names):
            length = len(self.list_entry_names)-1
            while length+1:
                self.list_entry_precents[length].destroy()
                self.list_entry_names[length].destroy()
                length -= 1
                
            self.list_entry_precents = []
            self.list_entry_names = []

        for i in range(num):
            self.list_entry_names.append(ttk.Entry(self, justify='center'))
            if i < len(self.list_names):
                self.list_entry_names[i].insert(0, self.list_names[i])
            else:
                self.list_entry_names[i].insert(0, 'Бумага')
            self.list_entry_names[i].grid(row=i+1, column=1, sticky=tk.W, pady=5, padx=5)

            self.list_entry_precents.append(ttk.Entry(self, justify='center'))
            if i < len(self.list_precents):
                self.list_entry_precents[i].insert(0, self.list_precents[i])
            else:
                self.list_entry_precents[i].insert(0, 0)
            self.list_entry_precents[i].grid(row=i+1, column=2, sticky=tk.W, pady=5, padx=5)

        self.btn_save.destroy()
        self.btn_save = tk.Button(self, text='Сохранить', width=15, command=self.save)
        self.btn_save['bg'] = 'white'
        self.btn_save.grid(row=int(self.entery_num.get())+2, column=2, pady=5, padx=5)
        


    def save(self):
        df = pd.DataFrame(columns=['Name', 'Precent'])
        names = [item.get() for item in self.list_entry_names]
        precents = [item.get() for item in self.list_entry_precents]
        df.loc[:, 'Name'] = names
        df.loc[:, 'Precent'] = precents
        df.to_csv('papers.csv', index=False)
        self.destroy()
        root.destroy()




if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    #app.pack()
    root.title("Инвестиционный Портфель")
    root.geometry("+570+180")
    root.resizable(False, False)
    root.mainloop()