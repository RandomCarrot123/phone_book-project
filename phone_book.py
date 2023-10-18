import tkinter as tk
from tkinter import ttk
import sqlite3


# Класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # Инициализация виджетов главного окна
    def init_main(self):
        # Верхняя панель для кнопок
        # bg - фон
        # bd - границы
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        # Упаковка
        # side - закрепляет вверху окна
        # fill - растягивает по X (горизонтали)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопка добавления
        # file - путь к файлу
        self.add_img = tk.PhotoImage(file='./add.png')
        # bg - фон
        # bd - границы
        # image - иконка кнопки
        # command - функция по нажатию
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0',bd=0,
                                    image=self.add_img,
                                    command=self.open_dialog)
        # Упаковка и выравнивание по левому краю
        btn_open_dialog.pack(side=tk.LEFT)

        # Кнопка изменения данных
        self.update_img = tk.PhotoImage(file='./update.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, 
                                    image=self.update_img,
                                    command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        # Кнопка удаления записи
        self.delete_img = tk.PhotoImage(file='./delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                               image=self.delete_img,
                               command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        # Кнопка поиска
        self.search_img = tk.PhotoImage(file='./search.png')
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                               image=self.search_img,
                               command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        # Кнопка обновления
        self.refresh_img = tk.PhotoImage(file='./refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                                image=self.refresh_img,
                                command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # Создание Treeview (таблица контактов)
        # columns - столбцы
        # height - высота таблицы
        # show='headings' скрываем нулевую (пустую) колонку таблицы
        self.tree = ttk.Treeview(self,
                                 columns=('ID','name', 'phone', 'email'),
                                 height=45,
                                 show='headings')
        # Параметры колонок
        # width - ширина
        # anchor - выравнивание текста в ячейке
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("phone", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)

        # Подписи колонок
        self.tree.heading("ID", text='ID')
        self.tree.heading("name", text='ФИО')
        self.tree.heading("phone", text='Телефон')
        self.tree.heading("email", text='E-mail')

        # Упаковка
        self.tree.pack(side=tk.LEFT)

        # Создание ползунка
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # Метод для записи новых данных в БД
    def records(self, name, phone, email):
        self.db.insert_data(name, phone, email)
        self.view_records()

    # Метод для обновления (изменения) данных
    def update_record(self, name, phone, email):
        self.db.c.execute('''UPDATE users SET name=?, phone=?, email=? WHERE ID=?''',
        (name, phone, email, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    # Метод для удаления записей
    def delete_records(self):
        # Цикл по выделенным записям
        for phoneion_item in self.tree.selection():
            # Удаление из БД
            self.db.c.execute('''DELETE FROM users WHERE id=?''',
            (self.tree.set(phoneion_item, '#1'),))
        # Сохранение изменений в БД
        self.db.conn.commit()
        # Обновление виджета таблицы
        self.view_records()

    # Вывод данных в виджет таблицы
    def view_records(self):
        # Выбираем информацию из БД
        self.db.c.execute('''SELECT * FROM users''')
        # Удаляем всё из виджета таблицы
        [self.tree.delete(i) for i in self.tree.get_children()]
        # Добавляем в виджет таблицы всю информацию из БД
        [self.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]

    # поиск записи
    def search_records(self, name):
        name = ('%' + name + '%',)
        self.db.c.execute('''SELECT * FROM users WHERE name LIKE ?''', name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
        for row in self.db.c.fetchall()]

    # Метод отвечающий за вызов дочернего окна
    def open_dialog(self):
        Child()

    # Метод отвечающий за вызов окна для изменения данных
    def open_update_dialog(self):
        Update()

    # Метод отвечающий за вызов окна для поиска
    def open_search_dialog(self):
        Search()

# Класс дочерних окон
# Toplevel - окно верхнего уровня
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # Инициализация виджетов дочернего окна
    def init_child(self):
        # Заголовок окна
        self.title('Добавить')
        # Размер окна
        self.geometry('400x220')
        # Запрет на изменение размеров окна
        self.resizable(False, False)

        # Перехватываем все события происходящие в приложении
        self.grab_set()
        # Захватываем фокус
        self.focus_set()

        # Добавляем подписи
        # text - название
        # x, y - координаты объекта
        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text='Телефон')
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text='E-mail')
        label_email.place(x=50, y=110)

        # Добавляем строки ввода
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)


        # Кнопка закрытия дочернего окна
        self.btn_cancel = ttk.Button(self, text='Закрыть',
                                     command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        # Кнопка добавить
        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        # <Button-1> - срабатывание по ЛКМ
        # При нажатии кнопки вызывается метод records, которому передаюся значения из строк ввода
        self.btn_ok.bind('<Button-1>', lambda event:
        self.view.records(self.entry_name.get(),
                          self.entry_phone.get(),
                          self.entry_email.get()))
    

# Класс окна для обновления, наследуемый от класса дочернего окна
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event:
        self.view.update_record(self.entry_name.get(),
                                self.entry_phone.get(),
                                self.entry_email.get()))

        # Закрываем окно редактирования
        # add='+' позволяет на одну кнопку вешать более одного события
        btn_edit.bind('<Button-1>', lambda event:
        self.destroy(), add='+')
        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM users WHERE id=?''',
        (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        # Получаем доступ к первой записи из выборки
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])


# Класс поиска записи
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event:
        self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event:
        self.destroy(), add='+')


# Класс БД
class DB:
    def __init__(self):
        # Создаем соединение с БД
        self.conn = sqlite3.connect('contacts.db')
        # Создание объекта класса cursor, используемый для взаимодействия с БД
        self.c = self.conn.cursor()
        # Выполнение запроса к БД
        self.c.execute('''CREATE TABLE IF NOT EXISTS users (
            id integer primary key,
            name text,
            phone text,
            email text)''')
        # Сохранение изменений БД
        self.conn.commit()

    # Метод добавления в БД
    def insert_data(self, name, phone, email):
        self.c.execute('''INSERT INTO users (name, phone, email)
                       VALUES (?, ?, ?)''', (name, phone, email))
        self.conn.commit()




if __name__ == '__main__':
    root = tk.Tk()
    # Экземпляр класса DB
    db = DB()
    app = Main(root)
    app.pack()
    # Заголовок окна
    root.title('Телефонная книга')
    root.geometry('665x450')
    root.resizable(False, False)
    root.mainloop()