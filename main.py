from tkinter import *
from tkinter import scrolledtext, messagebox
import sqlite3
import PyPDF2


# Немного баз данных
# region BD
def createBook(id, author, book, content):
    try:
        conn = sqlite3.connect('C:/Users/qwert/AppData/Local/Programs/Python/Python311/testbooks.db')
        cur = conn.cursor()
        print("Соединение с SQLite установлено")

        cur.execute("""INSERT or replace INTO Books(id, nameofauthor, nameofbooks, content) 
        VALUES('{}', '{}', '{}', '{}');""".format(id, author, book, content))
        conn.commit()
        cur.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if conn:
            conn.close()
            print("Соединение с SQLite закрыто")

def proverkaAuthor(nameofauthor, nameofbooks):
    try:
        conn = sqlite3.connect('C:/Users/qwert/AppData/Local/Programs/Python/Python311/testbooks.db')
        cur = conn.cursor()
        print("Соединение с SQLite установлено")

        sql_select_query = """select * from Books where nameofauthor = ? and nameofbooks = ?"""
        cur.execute(sql_select_query, (nameofauthor, nameofbooks))
        one_result = cur.fetchall()
        for row in one_result:
            n = 1

        cur.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if conn:
            conn.close()
            print("Соединение с SQLite закрыто")
    return row[3]

# endregion

window = Tk()

def btn_click_author():
    try:
        author = AuthorInput.get()
        book = BookInput.get()
        txet.delete("1.0", "end")
        txet.insert(INSERT, proverkaAuthor(author, book))
    except:
        messagebox.showerror(title='Ошибка при поиске', message='Такой книги в системе нет, возможно вы ошиблись.')



def btn_click_new_file():

    try:
        bookpath = pathInput.get()
        id = idInput.get()
        book = NameBookInput.get()
        author = NameAuthor.get()

        with open('{}'.format(bookpath), 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)

            for page_num in range(pdf_reader.numPages):
                pdf_page = pdf_reader.getPage(page_num)
                content = pdf_page.extractText()
        createBook(id, author, book, content)
        NameAuthor.delete(0, "end")
        NameBookInput.delete(0, "end")
        idInput.delete(0, "end")
        pathInput.delete(0, "end")
        messagebox.showinfo(title='Успешно', message='Книга добавилась!')
    except:
        messagebox.showerror(title='Ошибка при добавлении', message='Какая-то проблема')


# Немного дизайна
# region Design
window.title("Читалка")
window['bg'] = "gray"
window.wm_attributes('-alpha', 0.9)
window.geometry('700x800')
#window.resizable(width=False, height=False)

# endregion


# Немного Интерфейса
# region Interface
frameNewBook = Frame(window, bg='white')
frameNewBook.place(relheight=0.20, relwidth=1)

lbl1 = Label(frameNewBook,text="Путь к файлу:", bg='white')
lbl1.grid(column=0, row=0)
pathfile = StringVar()
#Текстовое поля для пути к файлу
pathInput = Entry(frameNewBook, textvariable=pathfile, bg='white')
pathInput.grid(column=1, row=0)

lbl2 = Label(frameNewBook,text="ID книги:", bg='white')
lbl2.grid(column=0, row=1)
#Текстовое поле для id книги
idBook = StringVar()
idInput = Entry(frameNewBook, textvariable=idBook, bg='white')
idInput.grid(column=1, row=1)

lbl3 = Label(frameNewBook,text="Фамиилия автора:", bg='white')
lbl3.grid(column=0, row=2)
#Текстовое поле для фамилии автора
nameAuthor = StringVar()
NameAuthor = Entry(frameNewBook, textvariable=nameAuthor, bg='white')
NameAuthor.grid(column=1, row=2)

lbl4 = Label(frameNewBook,text="Название книги:", bg='white')
lbl4.grid(column=0, row=3)
#Текстовое поле для названия книги
nameBook = StringVar()
NameBookInput = Entry(frameNewBook, textvariable=nameBook, bg='white')
NameBookInput.grid(column=1, row=3)

#Кнопка добавить книгу
pathButton = Button(frameNewBook, text="Добавить книгу", bg='white', command=btn_click_new_file)
pathButton.grid(column=4, row=3)

#Поиск по автору
messageAuthor = StringVar()
frameAuthor = Frame(window, bg='white')
frameAuthor.place(relheight=0.15, relwidth=1,rely=0.20)
lbl5 = Label(frameAuthor,text="Фамилия:", bg='white')
lbl5.grid(column=0, row=0)
AuthorInput = Entry(frameAuthor, textvariable=messageAuthor, bg='white')
AuthorInput.grid(column=1, row=0)
messageBook = StringVar()
lbl5 = Label(frameAuthor,text="Название:", bg='white')
lbl5.grid(column=0, row=1)
BookInput = Entry(frameAuthor, textvariable=messageBook, bg='white')
BookInput.grid(column=1, row=1)
buttonAuthor = Button(frameAuthor, text="Поиск книги", bg='white', command=btn_click_author)
buttonAuthor.grid(column=6, row=1)



# frame for text
frameContent = Frame(window, bg='white')
frameContent.place(rely=0.30, relheight=0.70, relwidth=1)



txet = scrolledtext.ScrolledText(frameContent, width=400, height=40, bg='white')
txet.pack()
# endregion


window.mainloop()
