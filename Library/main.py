from tkinter import *
from tkinter import messagebox, PhotoImage
from tkinter import filedialog
import sqlite3

WINDOW_TITLE = "Книжный магазин"
WINDOW_GEOMERTY = "300x215"
LABEL_ID_BOOK = "id книги: "
LABEL_NAME_BOOK = "Название книги: "
LABEL_AUTHOR = "Автор: "
LABEL_PRICE = "Цена: "
LABEL_DEL_BY_ID = "Удаление элемента по id: "
TEXT_BUTTON_EDIT = "Добавить"
TEXT_BUTTON_DEL = "Удалить"
TEXT_CREATE_FILE = "Создать БД"
TEXT_OPEN_FILE = "Открыть БД"
SHOW_DATA = "Содержимое БД"
NAMETABLE = "Books"
nameDB = "database.db"
BUTTON_COLOR = "#E6E6FA"
WINDOW_COLOR = "#777777"
ACT_BUTTON_COLOR = "#B0C4DE"
LABEL_BG = "#777777"
UPDATE_DATA = "Редактировать данные"


class Database:
    def __init__(self, nameDB):
        self.db = sqlite3.connect(nameDB)  # Если файл не был создал или открыт по дефолту создастся файл database.txt
        self.cursor = self.db.cursor()

    def create_table(self, table):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS '{table}' (\
                            book_id INTEGER PRIMARY KEY, \
                            book_name TEXT, \
                            author_name TEXT, \
                            price INTEGER)")

    def save(self):
        self.db.commit()

    def get_table(self, table):
        return [i for i in self.cursor.execute(f"SELECT * FROM {table}")]


class Window:
    def __init__(self):
        self.window = Tk()
        self.window.title(WINDOW_TITLE)
        self.window.geometry(WINDOW_GEOMERTY)
        self.window["bg"] = WINDOW_COLOR
        self.id_book = StringVar()  # Присваивает строку из виджета поля для ввода текста
        self.name_book = StringVar()
        self.author = StringVar()
        self.book_price = StringVar()
        self.id_book_del = StringVar()  # примечание разработчика переменная возможно не нужена
        self.background_image = PhotoImage(file="LNT.png")
        self.upd_book_name = StringVar()
        self.upd_author = StringVar()
        self.upd_price = StringVar()
        self.top_menu()
        self.main_menu()

    def show_data(self):
        db = Database(nameDB)
        win = Toplevel(self.window)
        win.geometry('500x250')
        win['bg'] = WINDOW_COLOR
        titles_columns = ['id', 'Назвние книги', 'Имя автора', 'Цена']
        for i in range(len(titles_columns)):
            titles = Entry(win, font='Calibri 9 bold', width=20)
            titles.insert(0, titles_columns[i])
            titles.grid(row=0, column=i)
        book_list = [i for i in db.cursor.execute(f"SELECT * FROM {NAMETABLE}")]
        col = len(book_list)
        row = 4
        for i in range(col):
            for j in range(row):
                b = Entry(win)
                b.insert(0, book_list[i][j])
                b.grid(row=i+1, column=j)

    def top_menu(self):
        menu = Menu(self.window)  # создаем объект меню для секций
        menu.add_cascade(label=TEXT_CREATE_FILE, command=creat_db)
        menu.add_cascade(label=TEXT_OPEN_FILE, command=open_db)
        menu.add_cascade(label=SHOW_DATA, command=self.show_data)
        menu.add_cascade(label=UPDATE_DATA, command=self.editing_window)
        menu.add_cascade(label="О программе", command=lambda: messagebox.showinfo("О программе", "Разработал Митюшин Пётр и Андрей Слепов."))  # Меню о программе добавляется на панель меню
        self.window.config(menu=menu)  # доступ к атрибуту объекта после его инициализации

    def create_label(self, text_label, x_label, y_label):   # Функция принимает строку и координаты
        Label(text=text_label, bg=LABEL_BG).place(x=x_label, y=y_label)  # Отображает текст в окне по переданным координатам

    def main_menu(self):  # Функция отображения полей ввода в главном меню
        global idb
        self.create_label(LABEL_ID_BOOK, 40, 0)  # Отображаем текст хранящейся в переменной label_id_book
        idb = Entry(width=20, textvariable=self.id_book).place(x=5, y=20) # Определим элемент Entry который представляет собой поле для ввода текста

        self.create_label(LABEL_NAME_BOOK, 20, 40)
        book = Entry(width=20, textvariable=self.name_book).place(x=5, y=60)

        self.create_label(LABEL_AUTHOR, 45, 80)
        author = Entry(width=20, textvariable=self.author).place(x=5, y=100)

        self.create_label(LABEL_PRICE, 45, 120)
        price = Entry(width=20, textvariable=self.book_price).place(x=5, y=140)

        Button(self.window, text=TEXT_BUTTON_EDIT, command=insert_data, bg=BUTTON_COLOR, activebackground=ACT_BUTTON_COLOR).place(x=35, y=165)

        self.create_label(LABEL_DEL_BY_ID, 140, 120)
        delete = Entry(width=24, textvariable=self.id_book_del).place(x=140, y=140)

        Button(self.window, text=TEXT_BUTTON_DEL, width=10, command=delete_book_by_id, bg=BUTTON_COLOR, activebackground=ACT_BUTTON_COLOR).place(x=175, y=165)

        print("BUILD SUCCESSFUL!")
        background = Label(self.window, image=self.background_image, width=100, height=108).place(x=160, y=5)

    def editing_window(self):
        global lb
        global win_update
        db = Database(nameDB)
        win_update = Toplevel(self.window)
        win_update.geometry('480x230')
        win_update['bg'] = WINDOW_COLOR

        book_list = [i for i in db.cursor.execute(f"SELECT * FROM {NAMETABLE}")]
        lb = Listbox(win_update, width=50, font=14)

        for book in book_list:
            book_str = " ".join([str(field) for field in book])
            lb.insert(END, book_str)
        lb.pack()

        change_button = Button(win_update, text="Изменить", bg=BUTTON_COLOR, activebackground=ACT_BUTTON_COLOR,
                             command=self.create_upd_window).place(x=400, y=200)

    def create_upd_window(self):    #
        global win_update
        upd_window = Toplevel(win_update)
        upd_window.geometry('450x100')
        upd_window['bg'] = WINDOW_COLOR

        Label(upd_window, text=LABEL_NAME_BOOK, bg=LABEL_BG).place(x=0, y=3)
        Entry(upd_window, width=20, textvariable=self.upd_book_name).place(x=0, y=20)

        Label(upd_window, text=LABEL_AUTHOR, bg=LABEL_BG).place(x=150, y=3)
        Entry(upd_window, width=20, textvariable=self.upd_author).place(x=150, y=20)

        Label(upd_window, text=LABEL_PRICE, bg=LABEL_BG).place(x=300, y=3)
        Entry(upd_window, width=20, textvariable=self.upd_price).place(x=300, y=20)
        done_button = Button(upd_window, text="OK", bg=BUTTON_COLOR, activebackground=ACT_BUTTON_COLOR,
                             command=update_data).place(x=400, y=42)


def update_data():  # Редактирование данных
    db = Database(nameDB)
    try:
        selection = lb.curselection()
        select = lb.get(selection[0])
        select_item = list(select.split())
    except IndexError:
        messagebox.showinfo("Error", "You are not select book")
    if(str(window.upd_price.get()).isdigit()):
        db.cursor.execute("""UPDATE `books` 
                          SET `book_name` = (?),
                          `author_name` = (?),
                          `price` = (?)
                          WHERE `book_id` = (?)
                    """, (window.upd_book_name.get(), window.upd_author.get(), window.upd_price.get(), select_item[0]))
    else:
        messagebox.showerror("Error", "Price can only contain numbers")
    db.save()
    win_update.destroy()


def creat_db():  # При вызове функции открывается диалоговое окно, где в поле имя файлов надо ввести имя файла которое вы хотите создать
    global nameDB
    path_db = filedialog.asksaveasfilename(initialdir="/", title="Select file", filetypes=(("database files", "*.db"), ("all files", "*.*")))
    nameDB = path_db
    db = Database(nameDB)
    db.create_table(NAMETABLE)


def delete_book_by_id():
    db = Database(nameDB)
    cursor = db.cursor
    cursor.execute('DELETE FROM {0} WHERE book_id = {1}'.format(NAMETABLE, window.id_book_del.get()))
    db.save()


def insert_data():
    db = Database(nameDB)
    if (str(window.id_book.get()).isdigit() and str(window.book_price.get()).isdigit()):
        db.cursor.execute("INSERT INTO books (book_id, book_name, author_name, price) VALUES (?,?,?,?)",
            (window.id_book.get(), window.name_book.get(), window.author.get(), window.book_price.get()))
        db.save()
    else:
        messagebox.showerror("Error", "Id and price can only contain numbers")


def open_db():  # При вызове функции открывается диалоговое окно, где пользователь выбирает какой файл ему нужно открыть
    global nameDB
    path_db = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("database files", "*.db"), ("all files", "*.*")))  # op является путём и его надо передать в функции добавления и удаления из файла
    nameDB = path_db


window = Window()
mainloop()  # Отображает главное окно со всеми виджетами
