from tkinter import Tk, NO, LEFT, RIGHT, W, Toplevel, StringVar, END, TOP, Label, Menu, Button, X, Y, E
from tkinter.ttk import Treeview, Frame, LabelFrame, Entry, Scrollbar
from tkinter.filedialog import askopenfilename as fn
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter.filedialog import askopenfilename as of
from tkinter.messagebox import showerror as se
from indicators import indicators
import sys

from cl_math import belong_total


class App:

    def __init__(self):
        self.evaluate_df = None
        self.balance = None
        self.balance_df = None
        self.company_name = None
        self.metric_df = pd.read_pickle('stand_set.pkl')
        self.v1, self.v2 = 0, 0

        self.window = Tk()
        window_x, window_y = 900, 470
        self.window.title('Классификатор')
        self.window.geometry('{}x{}'.format(window_x, window_y))
        self.window.minsize(window_x, window_y)
        self.window.maxsize(window_x, window_y)

        mainmenu = Menu(self.window)
        self.window.config(menu=mainmenu)
        mainmenu.add_command(label='Загрузить', command=lambda c=self.window: self.load_table(c))
        mainmenu.add_command(label='Выйти', command=lambda x=0: sys.exit(x))

        left = Frame(self.window)
        right = Frame(self.window)
        eval_c = LabelFrame(right, text='  Оценка компании')
        eval_f = LabelFrame(right, text='  Функции принадлежности')

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=left)
        self.canvas.draw()

        toolbar = NavigationToolbar2Tk(self.canvas, left, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(side=TOP)
        self.canvas.get_tk_widget().pack(side=TOP)

        self.evaluate_df = None

        c_chooser = Frame(eval_c)

        Label(c_chooser, text='Компания').pack(side=LEFT, padx=(10, 0), pady=(10, 10))
        self.company = Label(c_chooser, text='---', width=31)
        self.company.pack(side=LEFT, padx=(8, 5), pady=(10, 10))

        c_chooser.pack(side=TOP, anchor=W)

        self.p_names = list(pd.read_excel('p_names.xlsx', header=None)[0])

        p_frame = Frame(eval_c)

        columns = ('#1', '#2')
        self.params = Treeview(p_frame, show='headings', columns=columns, height=12, selectmode='browse')
        self.params.heading('#1', text='Параметр')
        self.params.heading('#2', text='Значение')
        self.params.column('#1', width=250, minwidth=250, stretch=NO, anchor=W)
        self.params.column('#2', width=80, minwidth=80, stretch=NO, anchor=E)
        vsb = Scrollbar(p_frame, orient="vertical", command=self.params.yview)

        self.params.configure(yscrollcommand=vsb.set)
        self.params.pack(side=LEFT)
        vsb.pack(side=LEFT, fill=Y)
        p_frame.pack(side=TOP, padx=(5, 5), pady=(0, 10))

        self.risk = Label(eval_f, text='', justify=LEFT)
        self.risk.pack(side=TOP, anchor=W, padx=(10, 0), pady=(10, 5))
        self.well = Label(eval_f, text='')
        self.well.pack(side=TOP, anchor=W, padx=(10, 0), pady=(0, 10))

        if self.evaluate_df is not None:
            self.update_treeview()
            self.update_draw()

        left.pack(side=LEFT)
        eval_c.pack(side=TOP)
        eval_f.pack(side=TOP, pady=(15, 0), fill=X)
        right.pack(side=LEFT, padx=(20, 10), pady=(10, 10))

        self.base_draw()

        self.window.mainloop()

    def base_draw(self):
        self.ax.clear()
        self.ax.scatter(self.metric_df['Зона риска'], self.metric_df['Зона благополучия'],
                        c=self.metric_df.cluster, s=20, cmap='inferno')
        self.ax.set_xlabel("Принадлежность к зоне риска")
        self.ax.set_ylabel("Принадлежность к зоне благополучия")
        self.canvas.draw()

    def update_treeview(self, event=None):
        for x in self.params.get_children():
            self.params.delete(x)
        for index, row in self.evaluate_df.iterrows():
            self.params.insert("", END, values=[row['key'], int(row['value'] * 1000) / 1000])
        self.v1, self.v2 = belong_total(list(self.evaluate_df['value'].values))
        self.risk['text'] = 'Зона риска {:5.2f}'.format(self.v1)
        self.well['text'] = 'Зона благополучия {:5.2f}'.format(self.v2)

    def update_draw(self, event=None):
        self.ax.scatter(self.metric_df['Зона риска'], self.metric_df['Зона благополучия'], c=self.metric_df.cluster,
                        s=20, cmap='inferno')
        self.ax.set_xlabel("Принадлежность к зоне риска")
        self.ax.set_ylabel("Принадлежность к зоне благополучия")
        self.ax.scatter([self.v1], [self.v2], c='red', s=40)
        self.canvas.draw()

    def load_table(self, mainwindow):
        self.w = Toplevel()
        self.w.geometry('400x460')
        self.w.title('Загрузка данных баланса')

        data_frame = LabelFrame(self.w, text='Данные')

        label_frame = Frame(data_frame)
        Label(label_frame, text='Файл баланса').pack(side=TOP, padx=(10, 10), pady=(10, 10))
        Label(label_frame, text='Компания').pack(side=TOP, padx=(10, 10), pady=(0, 10), anchor=W)

        entry_frame = Frame(data_frame)
        self.file_name = StringVar(self.window)
        Entry(entry_frame, textvariable=self.file_name, width=26).pack(side=TOP, padx=(0, 10), pady=(10, 10))
        self.company_name = StringVar(self.window)
        Entry(entry_frame, textvariable=self.company_name, width=26).pack(side=TOP, padx=(0, 10), pady=(0, 10))

        label_frame.pack(side=LEFT,  padx=(10, 10), pady=(0, 0))
        entry_frame.pack(side=LEFT, padx=(10, 10), pady=(0, 0))

        button_frame = Frame(data_frame)
        Button(button_frame, text='...', command=self.choose_file).pack(side=TOP, padx=(0, 10), pady=(10, 10))
        button_frame.pack(side=LEFT)

        data_frame.pack(side=TOP, pady=(10, 10))

        tableframe=Frame(self.w)
        columns = ('#1', '#2')
        self.balance = Treeview(tableframe, show='headings', columns=columns, height=12, selectmode='browse')
        self.balance.heading('#1', text='Статья')
        self.balance.heading('#2', text='Значение')
        self.balance.column('#1', width=250, minwidth=252, stretch=NO, anchor=W)
        self.balance.column('#2', width=80, minwidth=80, stretch=NO, anchor=E)
        vsb = Scrollbar(tableframe, orient="vertical", command=self.params.yview)
        self.balance.configure(yscrollcommand=vsb.set)
        self.balance.pack(side=LEFT)
        vsb.pack(side=LEFT, fill=Y)
        tableframe.pack(side=TOP)

        buttonframe = Frame(self.w)
        Button(buttonframe, text='Загрузить', command=self.update_scatter, width=15).\
            pack(side=LEFT, padx=(10, 10), pady=(5, 5))
        Button(buttonframe, text='Закрыть', command=self.w.destroy, width=15).pack(side=LEFT, padx=(0, 10), pady=(5, 5))
        buttonframe.pack(side=TOP, pady=(10, 10))

    def update_scatter(self):
        values = self.balance_df[self.balance_df.columns[1]]

        # расчет показателей
        self.evaluate_df = indicators(values)
        self.company['text'] = self.company_name.get()
        self.update_treeview()
        self.update_draw()
        self.w.destroy()

    def choose_file(self):
        self.file_name.set(fn(title='Выберите файл баланса',
                              filetypes=(("MSExcel 2007", "*.xlsx"),
                                         ("MSExcel", "*.xls"))))
        self.balance_df = pd.read_excel(self.file_name.get(), index_col='Код')
        self.w.focus_force()
        cols = self.balance_df.columns
        for index, row in self.balance_df.iterrows():
            self.balance.insert("", END, values=[row[cols[0]], row[cols[1]]])

    def load_data(self):
        filename = of(filetypes=[("MS Excel files", "*.xlsx")])
        if filename:
            try:
                self.evaluate_df = pd.read_excel('to_evaluate.xlsx')
                self.update_treeview()
            except IOError:
                se(title='Ошибка чтения', message='Ошибка чтения файла данных')


if __name__ == '__main__':
    App()
