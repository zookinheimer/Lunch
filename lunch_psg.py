#!/usr/bin/env python3

import PySimpleGUI as sg
import random
import sqlite3
# from datetime import datetime
# from matplotlib.pyplot import fill
# from pathlib import Path

sg.ChangeLookAndFeel('SystemDefault')

lunch = ""
price = ""
lunch_price = ""

# list to provide options for adding a restaurant
options = [
    ("Cheap", "cheap"),
    ("Normal", "Normal")
]

# list options to choose from before rolling lunch
roll_options = [
    ("Cheap", "cheap"),
    ("Normal", "Normal")
]

# TODO: remove theme on buttons
layout= [
    [sg.Text(r"Click below to find out what's for Lunch")],
    [sg.Radio('Cheap', "lunch", default=True, key='cheap'), sg.Radio('Normal', "lunch", key='normal')],
    [sg.Button('Roll Lunch', key='roll', pad=5, use_ttk_buttons=None),
    sg.Button('Add Restaurant', key='add', pad=5, use_ttk_buttons=None),
    sg.Button('Delete Restaurant', key='delete', pad=5, use_ttk_buttons=None),
    sg.Button('List All', key='listall', pad=5, use_ttk_buttons=None),
    ]
]

mainscreen = sg.Window(
    'Lunch Program',
    layout,
    titlebar_icon='angry_pickle.ico',
    resizable=True,
    element_justification='c',
).Finalize()

# TODO: debug buttons not showing popup; sqlite function
while True:
    event, value = mainscreen.Read()
    if event in (None, 'Cancel'):
        break
    if event in (None, 'Roll Lunch'):
        if value['cheap'] == True:
            lunch = "Cheap"
        elif value['normal'] == True:
            lunch = "Normal"
        restaurant = random.choice(lunch)
        # random choice from lunch.db
        conn = sqlite3.connect('lunch.db')
        c = conn.cursor()
        c.execute("SELECT * FROM lunch WHERE lunch_type = ?", (lunch,))
        result = c.fetchall()
        conn.close()
        sg.Popup(result)
    if event in (None, 'Add Restaurant'):
        sg.Popup('Add a restaurant')
        sg.Popup('Enter the name of the restaurant')
        name = sg.PopupGetText('Name')
        sg.Popup('Enter the price of the lunch')
        price = sg.PopupGetText('Price')
        sg.Popup('Enter the lunch type')
        lunch = sg.PopupGetText('Lunch')
        conn = sqlite3.connect('lunch.db')
        c = conn.cursor()
        c.execute("INSERT INTO lunch VALUES (:name, :price, :lunch)",
                    {'name': name, 'price': price, 'lunch': lunch})
        conn.commit()
        conn.close()
    if event in (None, 'Delete Restaurant'):
        sg.Popup('Delete a restaurant')
        sg.Popup('Enter the name of the restaurant')
        name = sg.PopupGetText('Name')
        conn = sqlite3.connect('lunch.db')
        c = conn.cursor()
        c.execute("DELETE FROM lunch WHERE name = :name", {'name': name})
        conn.commit()
        conn.close()
    if event in (None, 'List All'):
        conn = sqlite3.connect('lunch.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM lunch")
        results = c.fetchall()
        conn.close()
        sg.Popup(results)
