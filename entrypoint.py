#!/usr/bin/env python3

from nicegui import app, ui
from util import (
    add_restaurant,
    delete_restaurant,
    get_all_restaurants,
    get_restaurants,
    rng_restaurant
)
from pathlib import Path

db_fn = Path(__file__).parent / "lunch.db"

# props = "full-width column inline justify-center items-center content-center"

# window
app.native.window_args = {
    'title': 'Lunch',
    'resizable': True,
}
app.native.start_args['debug'] = True

# tailwindcss / quasar classes
md_props = "w-full text-lg text-center"
ui.markdown("Click below to find out what's for **Lunch**").classes(md_props)

# radio selection
radio_props = "flex flex-row w-full justify-center items-center content-center"
radio = ui.radio(
    ["Cheap", "Normal"],
    value="Cheap").bind_enabled(lambda value: value).classes(radio_props)


def random_restaurant():
    """Return random restaurant based on cost."""
    option = radio.value.lower()
    restaurant = rng_restaurant(option)
    ui.notify(
        f"Today's {option} lunch is at {restaurant}",
        position="center",
        multi_line=True,
        close_button=True,
    )


def all_restaurants():
    """Return list of all restaurants."""
    option = radio.value.lower()
    restaurants = "\n".join([i for i in get_restaurants(option)])
    ui.notify(
        f"All {option} restaurants: {restaurants}",
        position="center",
        multi_line=True,
        close_button=True,
    )


# props('clearable').on('keydown.enter', lambda: ui.notify(f"Added {name.value} to {option} restaurants"))
# TODO: swith to context/dialog to prevent multiple buttons spawning when clicking the button
async def insert_restaurant():
    """Add restaurant to database."""
    option = radio.value.lower()
    # * works. mostly.
    # name = ui.input(
    #     label="Restaurant Name",
    #     placeholder="Restaurant Name",
    #     validation={'Input too long': lambda value: len(value) < 20}
    # ).props('clearable').on(
    #     'keydown.enter',
    #     lambda: add_restaurant((name.value).title(), option))
    # ! wip
    with ui.dialog() as dialog, ui.card():
        name = ui.input(
            label="Restaurant Name",
            placeholder="Restaurant Name",
            validation={'Input too long': lambda value: len(value) < 20}
        ).props('clearable').on(
            'keydown.enter',
            lambda: add_restaurant((name.value).title(), option))
        ui.button("Add", on_click=dialog.close)


# ! wip
async def show(func, *args, **kwargs):
    result = await dialog
    ui.notify(f"Added {name.value} to {option} restaurants")


def remove_restaurant():
    """Delete restaurant from database."""
    option = radio.value.lower()
    name = ui.input(
        label="Restaurant Name",
        placeholder="Restaurant Name",
        validation={'Input too long': lambda value: len(value) < 20}
    ).props('clearable').on(
        'keydown.enter',
        lambda: delete_restaurant((name.value).title()))


# row of buttons
button_props = "flex flex-row w-full justify-center items-center content-center"
with ui.row().classes(button_props):
    ui.button("Roll Lunch", on_click=random_restaurant)
    # ui.button("Add Restaurant", on_click=insert_restaurant) # TODO: place below row of buttons (only appears in web)
    ui.button("Add Restaurant", on_click=show(insert_restaurant))
    ui.button("Delete Restaurant", on_click=remove_restaurant)
    ui.button("List All", on_click=all_restaurants)


# website
ui.run(host="127.0.0.1")

# desktop
# ui.run(native=True, window_size=(640, 300), fullscreen=False)
