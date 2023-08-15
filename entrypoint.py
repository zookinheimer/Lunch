#!/usr/bin/env python3

from nicegui import app, ui, Client
from util import (
    add_restaurant,
    delete_restaurant,
    get_all_restaurants,
    get_restaurants,
    rng_restaurant
)
from pathlib import Path

db_fn = Path(__file__).parent / "lunch.db"


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


def update_database(*args):
    """Add/remove restaurant from database."""

    name = args[1]
    option = radio.value.lower()

    if args[0] == "add":
        add_restaurant(name, option)
    elif args[0] == "remove":
        delete_restaurant(name)
    ui.notify(
        f"{name} has been {args[0]}ed.",
        position="center",
        multi_line=True,
        close_button=True,
    )


# window
app.native.window_args = {
    'title': 'Lunch',
    'resizable': True,
}
app.native.start_args['debug'] = True


@ui.refreshable
def get_radio_value():
    """Return radio value (cheap/normal)."""

    radio_props = "flex flex-row w-full justify-center items-center content-center"
    global radio
    radio = ui.radio(
        ["Cheap", "Normal"],
        value="Cheap").bind_enabled(lambda value: value).classes(radio_props)
    return radio.value


@ui.page('/')
async def index(client: Client):
    """Main page."""

    # tailwindcss / quasar classes
    md_props = "w-full text-lg text-center"
    ui.markdown("Click below to find out what's for **Lunch**").classes(md_props)

    # radio selection
    radio = get_radio_value()

    # row of buttons
    button_props = "flex flex-row w-full justify-center items-center content-center"
    with ui.row().classes(button_props) as row:
        with row:
            # * display random restaurant on click
            ui.button("Roll Lunch", on_click=random_restaurant)

            # * add restaurant to database
            add_btn = ui.button("Add Restaurant", on_click=lambda value: "add")

            # * delete restaurant from database
            del_btn = ui.button("Delete Restaurant", on_click=lambda value: "remove")

            # * list all restaurants
            ui.button("List All", on_click=all_restaurants)

    # TODO: `bind_visibility` to button presses (add_btn, del_btn)
    with ui.row().classes(button_props) as form:
        # * add restaurant
        with form:
            add_input = ui.input(
                label="Add Restaurant",
                placeholder="Restaurant Name",
                validation={'Input too long': lambda value: len(value) < 25}
            ).props('clearable').on(
                'keydown.enter',
                lambda: update_database("add", (add_input.value).title())
            )

        # * delete restaurant
        with form:
            del_input = ui.input(
                label="Remove Restaurant",
                placeholder="Restaurant Name",
                validation={'Input too long': lambda value: len(value) < 25}
            ).props('clearable').on(
                'keydown.enter',
                lambda: update_database("remove", (del_input.value).title())
            )

# website
ui.run()

# desktop
# ui.run(native=True, window_size=(640, 300), fullscreen=False)
