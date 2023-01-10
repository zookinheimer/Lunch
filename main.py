#!/usr/bin/env python3

import flet as ft
# import random
# import sqlite3
# from datetime import datetime
from dataclasses import dataclass, field
from flet.buttons import RoundedRectangleBorder
from pathlib import Path
# from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional, Dict, List, Tuple

# TODO: import .util; connect to db; bind to buttons; create views based on button clicks

@dataclass
class CustomButton():
    text: str
    style: Tuple = field(default_factory=lambda: ft.ButtonStyle(shape={
        ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=2),
    }))

    def __call__(self, text):
        return ft.ElevatedButton(
                text=self.text,
                style=self.style,
            )


def main(page):
    page.title = "Lunch"
    page.window_min_height = 100
    page.window_min_width = 200
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.update()

    text = ft.Text()
    choice = ft.RadioGroup(
        content=ft.Row([
            ft.Container(ft.Radio(value="cheap", label="Cheap"), alignment=ft.alignment.center),
            ft.Container(ft.Radio(value="normal", label="Normal"), alignment=ft.alignment.center),
        ],
        alignment=ft.MainAxisAlignment.CENTER,)
    )
    page.add(ft.Text("Click below to find out what's for Lunch:"), choice, text) # btn

    r = ft.Row([
        ft.Container(CustomButton(text="Roll Lunch")(page), alignment=ft.alignment.center),
        ft.Container(CustomButton(text="Delete Restaurant")(page), alignment=ft.alignment.center),
        ft.Container(CustomButton(text="Add Restaurant")(page), alignment=ft.alignment.center),
        ft.Container(CustomButton(text="List All")(page), alignment=ft.alignment.center),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    page.add(r)


ft.app(target=main)
