#!/usr/bin/env python3

import sqlite3
import random
from datetime import datetime
from matplotlib.pyplot import fill
from tkinter import *
from tkinter import messagebox
from tkinter import ttk


# Creats Main/root window for program
root = Tk()
# Sets the title of programs and dispalys in window bar
root.title("Lunch Program")
# sets the favicon for window
root.iconbitmap('angry_pickle.ico')
# sets the default root window size
root.geometry("500x100")

# SQL creates database file if it doesn't already exist
try:
    # create a database or connect to one
    conn = sqlite3.connect('lunch.db')
    #create a database cursor
    c = conn.cursor()

    # create table only need to run once
    c.execute("""CREATE TABLE lunch_list(
        restaurants text UNIQUE,
        option text
    )""")

    # commit changes
    conn.commit()

    # close connectiong
    conn.close()

    # create a database or connect to one
    conn = sqlite3.connect('lunch.db')
    #create a database cursor
    c = conn.cursor()

    # create table only need to run once
    c.execute("""CREATE TABLE recent_lunch(
        restaurants text UNIQUE,
        date timestamp
    )""")

    # commit changes
    conn.commit()

    # close connectiong
    conn.close()
except:
    pass

# variables
lunch = ""
# variable for raidio button for adding restaurant
price = StringVar()
price.set("Normal")

# list to provide options for adding a restaurant
options = [
    ("Cheap", "cheap"),
    ("Normal", "Normal")
]

# variable for radio button when rolling lunch
lunch_price = StringVar()
lunch_price.set("Normal")

# list options to choose from before rolling lunch
roll_options = [
    ("Cheap", "cheap"),
    ("Normal", "Normal")
]

# Functions
def calculate_lunch():
    global lunch_label
    conn = sqlite3.connect('lunch.db')
    c = conn.cursor()
    c.execute("SELECT * FROM lunch_list")
    records = c.fetchall()
    lpg = lunch_price.get()
    if lpg == "cheap":
        cheap_list = []
        for record in records:
            if record[1] == 'cheap':
                cheap_list.append(record)
        lunch = random.choice(cheap_list)
        lunch_label = Label(root, text="                            ")
        lunch_label.grid(row=3, column=0, columnspan=4)
        lunch_label = Label(root, text=lunch[0])
        lunch_label.grid(row=3, column=0, columnspan=4)
    else:
        # if less than 15 total restaunts a random choice is made regardless of previous choices
        normal_list = []
        for record in records:
            if record[1] == 'Normal':
                normal_list.append(record)
        if len(normal_list) < 15:
            lunch = random.choice(normal_list)
            lunch_label = Label(root, text="                            ")
            lunch_label.grid(row=3, column=0, columnspan=4)
            lunch_label = Label(root, text=lunch[0])
            lunch_label.grid(row=3, column=0, columnspan=4)
        else:
        # if over 15 total restaurants are available a random choice is made with consideration of the previous 14 picked options
            c.execute("SELECT * FROM recent_lunch")
            records2 = c.fetchall()
            lunch = random.choice(normal_list)

            if len(records2) > 14:
                limit = abs(14 - len(records2))
                c.execute("DELETE FROM recent_lunch WHERE oid IN (SELECT oid FROM recent_lunch ORDER BY date LIMIT " + str(limit) + ")")
                c.execute("SELECT * FROM recent_lunch")
                records2 = c.fetchall()

            # create list of restaurants to check against for lunch roll preventing repeated restraunts over a 14 day period
            list = []
            for record in records2:
                list.append(record[0])
            while lunch[0] in list:
                lunch=random.choice(normal_list)

            c.execute("INSERT INTO recent_lunch VALUES (:restaurants, :date)",
                {
                    'restaurants': lunch[0],
                    'date': datetime.now()
                })
            lunch_label = Label(root, text="                           ")
            lunch_label.grid(row=3, column=0, columnspan=4)
            lunch_label = Label(root, text=lunch[0])
            lunch_label.grid(row=3, column=0, columnspan=4)

    conn.commit()
    conn.close()


def add_restaurant():
    col=0
    global add_entry
    global add_window
    add_window = Toplevel()
    add_window.title("Add Restaurant")
    add_window.iconbitmap('angry_pickle.ico')
    add_label = Label(add_window, text="Enter the name of the restaurant you would like to add")
    add_label.grid(row=0, column=0)
    add_entry = Entry(add_window, width=30)
    add_entry.grid(row=0, column=1)
    for text, mode in options:
        add_radio = Radiobutton(add_window, text=text, variable=price, value=mode)
        add_radio.grid(row=1, column=col)
        col+=1
    add_button = Button(add_window, text="Add Restaurant", command=add_restaurant_sql)
    add_button.grid(row=2, column=1)
    # key bindings
    add_window.bind('<Return>', add_restaurant_sql)


def add_restaurant_sql(event=None):
    try:
        conn = sqlite3.connect('lunch.db')
        c = conn.cursor()
        c.execute("INSERT INTO lunch_list VALUES (:restaurants, :option)",
            {
                'restaurants': add_entry.get(),
                'option': price.get()
            })
        conn.commit()
        conn.close()
        add_entry.delete(0, END)
    except sqlite3.IntegrityError:
        error = messagebox.showerror("Duplicate Entry", "Looks like you already added " + add_entry.get())
        Label(add_window, text=error).grid(row=0, column=0)


def delete_restaurant():
    global del_entry
    global del_window
    del_window = Toplevel()
    del_window.title("Delete Restaurant")
    del_window.iconbitmap('angry_pickle.ico')
    del_window.geometry("520x320")
    del_label = Label(del_window, text="Enter the number of the restaurant you would like to delete")
    del_label.grid(row=0, column=0)
    del_entry = Entry(del_window, width=30)
    del_entry.grid(row=0, column=1)
    del_button = Button(del_window, text="Delete Restaurant", command=del_restaurant_sql)
    del_button.grid(row=1, column=1)

    # Create Canvas to apply Scrollbar
    del_window_frame1 = Frame(del_window)
    del_window_frame1.grid(row=2, column=0, columnspan=3)

    del_window_canvas = Canvas(del_window_frame1)
    del_window_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    del_window_scrollbar = ttk.Scrollbar(del_window_frame1, orient=VERTICAL, command=del_window_canvas.yview)
    del_window_scrollbar.pack(side=RIGHT, fill=Y)

    del_window_canvas.configure(yscrollcommand=del_window_scrollbar.set)
    del_window_canvas.bind('<Configure>', lambda e: del_window_canvas.configure(scrollregion=del_window_canvas.bbox("all")))
    # bind mouse wheel
    def mousewheel(event):
        del_window_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    del_window_canvas.bind('<MouseWheel>', mousewheel)

    del_window_frame2 = Frame(del_window_canvas)

    del_window_canvas.create_window((0,0), window=del_window_frame2, anchor="nw")

    # generate restaurt list with prime key numbers
    conn = sqlite3.connect('lunch.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM lunch_list")
    records = c.fetchall()

    print_records = ''
    rvar=2
    for record in records:
        print_records = record[0]
        del_label = Label(del_window_frame2, text=str(record[2]) + "\t" + print_records)
        del_label.grid(row=rvar, column=0, sticky=W)
        rvar += 1
    #key bindings
    del_window.bind('<Return>', del_restaurant_sql)


def del_restaurant_sql(event=None):
    conn = sqlite3.connect('lunch.db')
    c = conn.cursor()
    c.execute("DELETE from lunch_list WHERE oid= " + del_entry.get())
    conn.commit()
    conn.close()
    del_entry.delete(0, END)


def list_all():
    conn = sqlite3.connect('lunch.db')
    c = conn.cursor()
    c.execute("SELECT * FROM lunch_list ORDER BY restaurants")
    records = c.fetchall()

    list_window = Toplevel()
    list_window.geometry("450x250")
    list_window.iconbitmap('angry_pickle.ico')
    list_window.title("Restaurants")
    #create canvas to apply scroll bar
    list_window_frame1 = Frame(list_window)
    list_window_frame1.pack(fill=BOTH, expand=1)

    list_window_canvas = Canvas(list_window_frame1)
    list_window_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    list_window_scrollbar = ttk.Scrollbar(list_window_frame1, orient=VERTICAL, command=list_window_canvas.yview)
    list_window_scrollbar.pack(side=RIGHT, fill=Y)

    list_window_canvas.configure(yscrollcommand=list_window_scrollbar.set)
    list_window_canvas.bind('<Configure>', lambda e: list_window_canvas.configure(scrollregion=list_window_canvas.bbox("all")))
    #bind mouse wheel
    def mousewheel(event):
        list_window_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    list_window_canvas.bind('<MouseWheel>', mousewheel)

    list_window_frame2 = Frame(list_window_canvas)

    list_window_canvas.create_window((0,0), window=list_window_frame2, anchor="nw")

    print_records = ''
    rvar=0
    for record in records:
        print_records = record[0]
        if record[1] == "cheap":
            list_label = Label(list_window_frame2, text=print_records)
            list_label.grid(row=rvar, column=0, sticky=W, padx=20)
            list_label_cheap = Label(list_window_frame2, text="\t" + record[1])
            list_label_cheap.grid(row=rvar, column=1)
        else:
            list_label = Label(list_window_frame2, text=print_records)
            list_label.grid(row=rvar, column=0, sticky=W, padx=20)
        rvar += 1
    conn.close()

# Root Widgets
intro_label = Label(root, text="Click below to find out what's for Lunch")
intro_label.grid(row=0, column=0, columnspan=4)

lunch_button1 = Button(root, text="Roll Lunch", command=calculate_lunch)
lunch_button1.grid(row=2, column=0, padx=(20,0))

lunch_button2 = Button(root, text="Add Restaurant", command=add_restaurant)
lunch_button2.grid(row=2, column=1)

lunch_button3= Button(root, text="Delete Restaurant", command=delete_restaurant)
lunch_button3.grid(row=2, column=2)

lunch_button4 = Button(root, text="List All", command=list_all)
lunch_button4.grid(row=2, column=3)

col1 = 1
for text, mode in roll_options:
    add_radio = Radiobutton(root, text=text, variable=lunch_price, value=mode)
    add_radio.grid(row=1, column=col1)
    col1 += 1

# start program loop.
root.mainloop()
