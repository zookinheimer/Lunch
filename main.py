#!/usr/bin/env python3

import flet as ft
from flet import (
    Column,
    Container,
    Dropdown,
    ElevatedButton,
    RoundedRectangleBorder,
    Page,
    Row,
    Text,
    UserControl,
    border_radius,
    colors,
    dropdown
)
import logging
import random
# import sqlite3
# from datetime import datetime
from util import create_db_and_tables, get_all_restaurants, get_restaurants, rng_restaurant
from dataclasses import dataclass, field
from decouple import config
from pathlib import Path
# from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional, Dict, List, Tuple

# log level
logging.basicConfig(level=logging.INFO)


@dataclass
class CustomButton():
    text: str
    style: Tuple = field(default_factory=lambda: ft.ButtonStyle(shape={
        ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=2),
    }))
    on_click: Optional[ft.ElevatedButton().on_click] = None

    def __call__(self, text):
        return ft.ElevatedButton(
                text=self.text,
                style=self.style,
                on_click=self.on_click,
            )


class Lunch(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.choice = None
        self.snack_bar = None
        self._build()


        if button.data == "roll":
        def on_click(self, button):
            self.roll_lunch(self.choice.value)
        elif button.data == "delete":
            self.delete_restaurant()
        elif button.data == "add":
            self.add_restaurant()
        elif button.data == "list":
            self.list_all()
        self.snack_bar = ft.SnackBar(
            content=ft.Text(f"{button.text} clicked!"),
            duration=ft.Duration(milliseconds=5000),
        )
        page.add(self.snack_bar)
        self.snack_bar.show()


    def _build(self):
        page = self.page
        page.title = "Lunch"
        page.background_color = colors.WHITE
        page.padding = 10

        choice = ft.RadioGroup(
            content=ft.Row([
                ft.Container(ft.Radio(value="cheap", label="Cheap"), alignment=ft.alignment.center),
                ft.Container(ft.Radio(value="normal", label="Normal"), alignment=ft.alignment.center),
            ],
            alignment=ft.MainAxisAlignment.CENTER,)
        )
        page.add(ft.Text("Click below to find out what's for Lunch:"), choice)

        # TODO: use inline row declaration instead of custom button class (QA)
        row = Row(
            controls=[
                Container(CustomButton(text="Roll Lunch")(page), alignment=ft.alignment.center, on_click=self.on_click, data="roll"),
                Container(CustomButton(text="Delete Restaurant")(page), alignment=ft.alignment.center, on_click=self.on_click, data="delete"),
                Container(CustomButton(text="Add Restaurant")(page), alignment=ft.alignment.center, on_click=self.on_click, data="add"),
                Container(CustomButton(text="List All")(page), alignment=ft.alignment.center, on_click=self.on_click, data="list"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        page.add(row)


def main(page: Page):
    page.title = "Lunch"
    page.window_width = 650
    page.window_height = 275
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # create application instance
    app = Lunch(page)

    # add application's root control to page
    page.add(app)


ft.app(target=main)
