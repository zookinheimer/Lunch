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
    # toggle input form visibility if open
    add_input.set_visibility(False)
    del_input.set_visibility(False)


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
    # toggle input form visibility if open
    add_input.set_visibility(False)
    del_input.set_visibility(False)


def update_database(*args):
    """Add/remove restaurant from database."""

    name = args[1]
    option = radio.value.lower()

    if args[0] == "add":
        result = add_restaurant(name, option)
        if result is False:
            return ui.notify(
                f"{name} already exists in database.",
                position="center",
                multi_line=True,
                close_button=True,
            )
    elif args[0] == "remove":
        result = delete_restaurant(name)
        if result is None:
            return ui.notify(
                f"{name} does not exist in database.",
                position="center",
                multi_line=True,
                close_button=True,
            )

    if args[0] == "add":
        msg = f"{name} has been {args[0]}ed."
    elif args[0] == "remove":
        msg = f"{name} has been {args[0]}d."

    ui.notify(
        msg,
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
            add_btn = ui.button(
                "Add Restaurant",
                on_click=lambda: (add_input.set_visibility(True), del_input.set_visibility(False))
            )

            # * delete restaurant from database
            del_btn = ui.button(
                "Delete Restaurant",
                on_click=lambda: (del_input.set_visibility(True), add_input.set_visibility(False))
            )

            # * list all restaurants
            ui.button("List All", on_click=all_restaurants)

    # TODO: clear input form on submit
    with ui.row().classes(button_props) as form:
        # * add restaurant
        with form:
            global add_input
            add_input = ui.input(
                label="Add Restaurant",
                placeholder="Restaurant Name",
                validation={'Input too long': lambda value: len(value) < 25}
            ).props('clearable').on(
                'keydown.enter',
                lambda: (update_database("add", (add_input.value)), add_input.set_visibility(False))
            )
            add_input.set_visibility(False)

        # * delete restaurant
        with form:
            global del_input
            del_input = ui.input(
                label="Remove Restaurant",
                placeholder="Restaurant Name",
                validation={'Input too long': lambda value: len(value) < 25}
            ).props('clearable').on(
                'keydown.enter',
                lambda: (update_database("remove", (del_input.value)), del_input.set_visibility(False))
            )
            del_input.set_visibility(False)


# website
ui.run()

# desktop
# ui.run(native=True, window_size=(640, 300), fullscreen=False)
