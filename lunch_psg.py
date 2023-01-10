#!/usr/bin/env python3

import PySimpleGUI as sg
import random
import re
import sqlite3
from datetime import datetime
from icecream import ic
# from pathlib import Path

sg.ChangeLookAndFeel('SystemDefault')
sg.SetOptions(
            button_color = sg.COLOR_SYSTEM_DEFAULT,
            text_color = sg.COLOR_SYSTEM_DEFAULT
)

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

layout= [
    [sg.Text(r"Click below to find out what's for Lunch")],
    [sg.Radio('Cheap', "lunch", key='cheap', default=True),
    sg.Radio('Normal', "lunch", key='normal')],
    [sg.Button('Roll Lunch', pad=5),
    sg.Button('Add Restaurant', pad=5),
    sg.Button('Delete Restaurant', pad=5),
    sg.Button('List All', pad=5),
    ],
]

mainscreen = sg.Window(
    'Lunch Program',
    layout,
    titlebar_icon='angry_pickle.ico',
    resizable=True,
    element_justification='c',
).Finalize()


# TODO: error handling for when a category is missing (IndexError) -- repro by deleting the last item in a category
def calculate_lunch(lunch_price):
    """
    Makes a random choice for lunch based on price point.

    "Cheap" will choose a random choice from list. If "Normal", it will
    choose a random option from the database if the number of entries
    are under 14; if over it will make a random choice against 2nd table
    and either reroll a new random choice or proceed with original option
    if it's present.
    """

    conn = sqlite3.connect('lunch.db')
    c = conn.cursor()
    c.execute("SELECT * FROM lunch_list")
    records = c.fetchall()
    try:
        if lunch_price == "cheap":
            cheap_list = []
            for record in records:
                if re.search(r'cheap', record[1], re.IGNORECASE):
                    cheap_list.append(record)
            lunch = random.choice(cheap_list)
        else:
            # if less than 15 total restaunts a random choice is made
            # regardless of previous choices
            normal_list = []
            for record in records:
                if re.search(r'normal', record[1], re.IGNORECASE):
                    normal_list.append(record)
            if len(normal_list) < 15:
                lunch = random.choice(range(len(normal_list)))
            else:
            # if over 15 total restaurants are available a random choice
            # is made with consideration of the previous 14 picked options
                c.execute("SELECT * FROM recent_lunch")
                records2 = c.fetchall()
                lunch = random.choice(normal_list)

                if len(records2) > 14:
                    limit = abs(14 - len(records2))
                    c.execute(
                        """
                        DELETE FROM recent_lunch
                        WHERE oid IN (SELECT oid
                        FROM recent_lunch
                        ORDER BY date
                        LIMIT """ + str(limit) + ")"
                    )
                    c.execute("SELECT * FROM recent_lunch")
                    records2 = c.fetchall()

                # create list of restaurants to check against for
                # lunch roll preventing repeated restraunts over a 14 day period
                list = []
                for record in records2:
                    list.append(record[0])
                while lunch[0] in list:
                    lunch = random.choice(normal_list)

                c.execute("INSERT INTO recent_lunch VALUES (:restaurants, :date)",
                    {
                        'restaurants': lunch[0],
                        'date': datetime.now()
                    })
                conn.commit()
    except (IndexError, UnboundLocalError):
        print("No lunch today")
        conn.commit()
        conn.close()
        exit()
    finally:
        conn.close()

    return lunch


# TODO: fix function. Fails to validate input accepting empty strings et al
def valid_name(name):
    """
    Checks if the name is valid.

    Checks if the name is valid by checking if it is a string and
    if it is not empty.
    """

    name_regex = re.compile(r'^[a-zA-Z0-9\s\!\'\"]*$')

    if not isinstance(name, str) and name != "":
        while not name_regex.match(name):
            sg.Popup("Please enter a valid restaurant name")
            name = sg.PopupGetText('Enter the name of the restaurant')

    name = name.strip().title()

    return name


while True:
    event, value = mainscreen.Read()
    if event in (None, 'Cancel'):
        break
    if event in (None, 'Roll Lunch'):
        if value['cheap'] == True:
            lunch_price = "cheap"
        elif value['normal'] == True:
            lunch_price = "normal"
        result = calculate_lunch(lunch_price)
        sg.Popup(result[0])

    if event in (None, 'Add Restaurant'):
        name = sg.PopupGetText('Enter the name of the restaurant')
        name_regex = re.compile(r'^[a-zA-Z0-9\s\!\'\"]*$')
        while not name_regex.match(name):
            sg.Popup("Please enter a valid restaurant name")
            name = sg.PopupGetText('Enter the name of the restaurant')
        name = name.strip().title()

        restaurant_type = sg.popup(
            title = 'Add Restaurant',
            button_color = None,
            custom_text = ('Cheap', 'Normal'),
            keep_on_top = True
        )

        if restaurant_type == 'Cheap':
            price = "cheap"
        elif restaurant_type == 'Normal':
            price = "normal"
        price = price.strip().title()

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
            continue

    # TODO: validate input (see: valid_name)
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

        list_all = []
        for result in results:
            list_all.append(result[0])
        # print(*list_all, sep='\n')
        # print('\n'.join(str(i) for i in list_all))

        layout = [
            [sg.Listbox(values=list_all, size=(20, len(list_all)))],
            [sg.Button('Okay', bind_return_key=True)]
        ]
        window = sg.Window('List All', layout)
        event, values = window.read()
        if event in (None, 'Okay'):
            window.close()

         # TODO: table view of results (currently a list)

