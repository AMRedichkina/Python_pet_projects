"""
To-Do List:
A program that allows users to add, view, and mark
items as complete on a to-do list.
"""

from tkinter import *
from tkinter import messagebox
import sqlite3 as sq

def add_task():
    word = txt_input.get()
    if not word.strip():
        messagebox.showinfo('Empty Entry', 'Enter task name')
        return
    task.append(word)
    cur.execute('INSERT INTO tasks VALUES (?)', (word,))
    list_update()
    txt_input.delete(0, 'end')

def list_update():
    clear_list()
    for i in task:
        lb_tasks.insert('end', i)

def del_one():
    try:
        val = lb_tasks.get(lb_tasks.curselection())
    except TclError:
        messagebox.showinfo('Cannot Delete', 'No Task Item Selected')
        return
    if val in task:
        task.remove(val)
        list_update()
        cur.execute('DELETE FROM tasks WHERE title = ?', (val,))

def delete_all():
    mb = messagebox.askyesno('Delete All', 'Are you sure?')
    if mb == True:
        task.clear()
        cur.execute('DELETE FROM tasks')
        list_update()

def clear_list():
    lb_tasks.delete(0, 'end')

def retrieve_db():
    task.clear()
    for row in cur.execute('SELECT title FROM tasks'):
        task.append(row[0])

if __name__ == "__main__":
    root = Tk()
    root.title('To-Do List App')
    root.geometry("250x450")
    conn = sq.connect('todo.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS tasks (title text)')
    task = []
    lbl_title = Label(root, text='To-Do List', font=('Helvetica', 18, 'bold'))
    lbl_title.pack(pady=10)
    lbl_task_show = Label(root, text='Enter task below :',
                          font=('Helvetica', 16))
    lbl_task_show.pack(pady=10)
    txt_input = Entry(root, width=25, bd="2", font="18")
    txt_input.pack(pady=10)
    btn_add_task = Button(root, text='Add task', width=20,
                          command=add_task, relief=RIDGE)
    btn_del_one = Button(root, text='Complete task', width=20,
                         relief=RIDGE, command=del_one)
    btn_del_all = Button(root, text='Complete all', width=20,
                         relief=RIDGE, command=delete_all)
    btn_exit = Button(root, text='Exit', width=20, relief=RIDGE, command=exit)

    btn_add_task.pack(pady=10)
    btn_del_one.pack(pady=10)
    btn_del_all.pack(pady=10)
    btn_exit.pack(pady=10)

    lb_tasks = Listbox(root, width=24, height=10,
                       selectmode='SINGLE', relief=RIDGE, bd="4", font="14")
    lb_tasks.pack(pady=10) 

    retrieve_db()
    list_update()
   
    root.mainloop()
    conn.commit()
    cur.close()
