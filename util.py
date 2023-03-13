#!/usr/bin/env python3

import random
# from icecream import ic
from datetime import datetime
from pathlib import Path
from sqlalchemy import Column, func, Table, Text, TIMESTAMP
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional, Dict, List, Tuple

# verbose icecream
# ic.configureOutput(includeContext=True)

metadata = SQLModel.metadata


t_lunch_list = Table(
    'lunch_list', metadata,
    Column('restaurants', Text, unique=True),
    Column('option', Text)
)


t_recent_lunch = Table(
    'recent_lunch', metadata,
    Column('restaurants', Text, unique=True),
    Column('date', TIMESTAMP)
)


db_fn = Path(__file__).parent / "lunch.db"
csv_fn = Path(__file__).parent / "restaurants.csv"

engine = create_engine(f"sqlite:///{db_fn.name}", echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_all_restaurants():
    with Session(engine) as session:
        statement = select(t_lunch_list)
        restaurants = session.exec(statement).all()
        # return [i for i in restaurants if print(i)]       # pretty print restaurants only
        return [i for i in restaurants]                     # return list of restaurant names


def get_restaurants(option):
    with Session(engine) as session:
        statement = select(t_lunch_list).where(func.lower(t_lunch_list.c.option) == option.lower()) # case insensitive
        restaurants = session.exec(statement).all()
        return [i for i in restaurants]


def rng_restaurant(option):
    with Session(engine) as session:
        statement = select(t_lunch_list).where(func.lower(t_lunch_list.c.option) == option.lower()) # case insensitive
        restaurants = session.exec(statement).all()
        return random.choice(restaurants)

# def calculate_lunch():
#     global lunch_label

#     # if less than 15 total restaunts a random choice is made regardless of previous choices
#     records = get_all_restaurants()
#     if len(records) < 15:
#         lunch_label = random.choice(records)
#         return lunch_label
#     # if over 15 total restaurants are available a random choice is made with consideration of the previous 14 picked options
#     elif len(records) > 14:
#         ...
#     # create list of restaurants to check against for lunch roll preventing repeated restraunts over a 14 day period


def main():
    create_db_and_tables()
    print(get_all_restaurants())
    print(get_restaurants("Normal"))
    print(rng_restaurant("Cheap"))


if __name__ == "__main__":
    main()
