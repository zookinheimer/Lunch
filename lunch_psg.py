#!/usr/bin/env python3

import PySimpleGUI as sg
import random
import sqlite3
# from datetime import datetime
from icecream import ic
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
    [sg.Radio('Cheap', "lunch", key='cheap', default=True),
    sg.Radio('Normal', "lunch", key='normal')],
    [sg.Button('Roll Lunch', pad=5, use_ttk_buttons=None),
    sg.Button('Add Restaurant', pad=5, use_ttk_buttons=None),
    sg.Button('Delete Restaurant', pad=5, use_ttk_buttons=None),
    sg.Button('List All', pad=5, use_ttk_buttons=None),
    ],
]

mainscreen = sg.Window(
    'Lunch Program',
    layout,
    titlebar_icon='angry_pickle.ico',
    resizable=True,
    element_justification='c',
).Finalize()

while True:
    event, value = mainscreen.Read()
    if event in (None, 'Cancel'):
        break
    if event in (None, 'Roll Lunch'):
        if value['cheap'] == True:
            lunch = "Cheap"
        elif value['normal'] == True:
            lunch = "Normal"
        # TODO: get list of restaurants from database (cf. `calculate_lunch`)
        # restaurant = random.choice()
        conn = sqlite3.connect('lunch.db')
        c = conn.cursor()
        c.execute(f"""SELECT * FROM lunch_list WHERE "option" LIKE '{lunch}'""")
        result = c.fetchall()
        conn.close()
        # TODO: table view
        sg.Popup(result)
    # TODO: validate input (e.g., empty string, non alphanumeric, etc.)
    # TODO: escape single quotes in `name` (cf. `'McDonald''s'`)
    if event in (None, 'Add Restaurant'):
        name = sg.PopupGetText('Enter the name of the restaurant')
        while name.isalnum() == False or name.isalpha() == False:
            sg.Popup("Please enter a valid restaurant name")
            name = sg.PopupGetText('Enter the name of the restaurant')

        price = (sg.PopupGetText('Cheap or Normal')).lower()
        while price != 'cheap' or price != 'normal':
            sg.Popup("Please enter a valid type of restaurant")
            price = sg.PopupGetText('Cheap or Normal')

        try:
            conn = sqlite3.connect('lunch.db')
            c = conn.cursor()
            c.execute("INSERT INTO lunch_list VALUES (:restaurants, :option)",
                        {'restaurants': name, 'option': price})
            conn.commit()
            conn.close()
            sg.Popup("Restaurant added successfully")
        except sqlite3.IntegrityError:
            sg.Popup('Restaurant already added')
    if event in (None, 'Delete Restaurant'):
        name = sg.PopupGetText('Delete a restaurant')
        conn = sqlite3.connect('lunch.db')
        c = conn.cursor()
        c.execute(f"""DELETE FROM lunch_list WHERE "restaurants" = '{name}'""")
        conn.commit()
        conn.close()
    if event in (None, 'List All'):
        conn = sqlite3.connect('lunch.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM lunch_list")
        results = c.fetchall()
        conn.close()
        # TODO: table view
        sg.Popup(results)
