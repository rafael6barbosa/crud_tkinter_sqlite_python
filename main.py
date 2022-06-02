from turtle import width
import pandas as pd
import sqlite3
from tkinter import *
from tkinter import ttk
from sqlalchemy import values

global conn, cursor
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

def treee():
    
    tree.delete(*tree.get_children())
    df = pd.read_sql_query("SELECT chave,valor FROM requirements", conn)
    df = df.reset_index()

    for index, row in df.iterrows():
        tree.insert('', index = index, values=(row["chave"], row["valor"]))


def update():
    
    curItem = tree.focus()
    dict = tree.item(curItem)["values"]
    dict2 = list(str(dict).split(","))
    chave = (dict2[0].replace("'","")).replace("[","")
    valor = str(vvalor.get())
    query = f"UPDATE requirements SET valor = '{valor}' WHERE trim(chave) = trim('{chave}');"
    cursor.execute(query)
    conn.commit()
    treee()


root = Tk()
root.title("Crixus: Cadastro de requirements SQLite")

vvalor = StringVar()
s=ttk.Style()
s.theme_use('clam')
s.configure('Treeview', rowheight=30)

tree = ttk.Treeview(root, selectmode="browse",columns=(1, 2), show='headings', height=9)
tree.pack(side=TOP)
tree.heading(1, text="chave")
tree.heading(2, text="valor")
tree.column("# 1", stretch=NO, width=100)
tree.column("# 2", stretch=NO, width=250)
forms = Frame( )
forms.pack(side=TOP)
fvalor = Entry(forms, textvariable = vvalor , width=58)
fvalor.grid(row=0,column=0, padx=10,pady=10,ipady=30)
buttons = Frame( )
buttons.pack(side=TOP)
btn_update = Button(buttons, width=50, text="Update", command=update)
btn_update.pack(side=TOP)



if __name__ == '__main__':
    root.after(100, treee)
    root.mainloop()
    