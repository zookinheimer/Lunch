#!/usr/bin/env python3

import random
# from icecream import ic
from datetime import datetime
from pathlib import Path
from sqlalchemy import Column, func, Integer, String, Table, Text, TIMESTAMP
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional, Dict, List, Tuple

# verbose icecream
# ic.configureOutput(includeContext=True)

metadata = SQLModel.metadata

t_lunch_list = Table(
    "lunch_list",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("restaurant", String, unique=True),
    Column("option", String),
)

t_recent_lunch = Table(
    'recent_lunch', metadata,
    Column('id', Integer, primary_key=True),
    Column('restaurant', Text),
    Column('date', TIMESTAMP)
)

db_fn = Path(__file__).parent / "lunch.db"
lunch_list_fn = Path(__file__).parent / "lunch_list.csv"
recent_lunch_fn = Path(__file__).parent / "recent_lunch.csv"

engine = create_engine(f"sqlite:///{db_fn.name}", echo=False)


def create_db_and_tables():
    """Create database and tables if they don't exist."""
    SQLModel.metadata.create_all(engine)
    if not db_fn.exists():
        with Session(engine) as session:
            with open(lunch_list_fn, "r") as f:
                for line in f:
                    if line.startswith("restaurant"):
                        continue
                    line = line.strip("\n")
                    line = line.split(",")
                    new_restaurant = t_lunch_list.insert().values(restaurant=line[0], option=line[1])
                    session.execute(new_restaurant)
            # populate recent_lunch table
            with open(recent_lunch_fn, "r") as f:
                for line in f:
                    if line.startswith("restaurant"):
                        continue
                    line = line.strip("\n")
                    line = line.split(",")
                    line[1] = datetime.strptime(line[1], "%Y-%m-%d %H:%M:%S.%f")
                    new_restaurant = t_recent_lunch.insert().values(restaurant=line[0], date=line[1])
                    session.execute(new_restaurant)
            session.commit()


def get_all_restaurants():
    """Return list of all restaurants."""
    with Session(engine) as session:
        statement = select(t_lunch_list.c.restaurant)
        restaurants = session.exec(statement).all()
        return [i for i in restaurants]


def get_restaurants(option):
    """Return list of restaurants based on cost."""
    with Session(engine) as session:
            statement = select(
                t_lunch_list.c.restaurant
                ).where(func.lower(t_lunch_list.c.option) == func.lower(option))
            restaurants = session.exec(statement).all()
            return [i for i in restaurants]


def rng_restaurant(option):
    """Return random restaurant based on cost."""
    with Session(engine) as session:
        statement = select(
            t_lunch_list.c.restaurant
            ).where(func.lower(t_lunch_list.c.option) == func.lower(option))
        restaurants = session.exec(statement).all()
        if not restaurants:
            return print(f"No restaurants found for {option}.")
        else:
            return random.choice(restaurants)


def add_restaurant(name, option):
    """Add restaurant to database."""
    with Session(engine) as session:
        print(f"Adding {name} to database.")
        statement = select(t_lunch_list).where(t_lunch_list.c.restaurant == name)
        restaurant = session.exec(statement).first()
        if restaurant:
            return print(f"{name} already exists in database.")
        else:
            new_restaurant = t_lunch_list.insert().values(restaurant=name, option=option)
            session.execute(new_restaurant)
            session.commit()
            return print(f"{name} added to database.")


def delete_restaurant(name):
    """Delete restaurant from database."""
    with Session(engine) as session:
        print(f"Deleting {name} from database.")
        statement = select(t_lunch_list.c.id).where(t_lunch_list.c.restaurant == name)
        restaurant_id = session.exec(statement).first()
        if not restaurant_id:
            return print(f"{name} does not exist in database.")
        else:
            statement = t_lunch_list.delete().where(t_lunch_list.c.id == restaurant_id)
            session.commit()
            return print(f"{name} deleted from database.")


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
    print(f"{'All restaurants:':<20} {get_all_restaurants()}")
    print(f"{'Normal restaurants:':<20} {get_restaurants('Normal')}")
    print(f"{'Cheap restaurants:':<20} {get_restaurants('Cheap')}")
    print(f"{'Random restaurant:':<20} {rng_restaurant('Normal')}")


if __name__ == "__main__":
    main()
