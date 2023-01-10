#!/usr/bin/env python3

# import random
# from icecream import ic
from pathlib import Path
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional, Dict, List, Tuple

from dataclasses import dataclass, field
from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, Table, Text
from sqlalchemy.orm import registry

# verbose icecream
# ic.configureOutput(includeContext=True)

mapper_registry = registry()
metadata = mapper_registry.metadata


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


@mapper_registry.mapped
@dataclass
class Restaurant:
    __tablename__ = 'restaurant'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(init=False, metadata={'sa': Column(Integer, primary_key=True)})
    restaurant: str = field(metadata={'sa': Column(String, nullable=False)})
    option: str = field(metadata={'sa': Column(String, nullable=False)})


db_fn = Path(__file__).parent / "lunch.db"
csv_fn = Path(__file__).parent / "restaurants.csv"

engine = create_engine(f"sqlite:///{db_fn.name}", echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_all_restaurants():
    with Session(engine) as session:
        statement = select(Restaurant)
        restaurants = session.exec(statement).all()
        return [i for i in restaurants if print(i.restaurant)]    # pretty print restaurants only
        return [i.restaurant for i in restaurants]                  # return list of restaurant names


def get_restaurants(option):
    with Session(engine) as session:
        statement = select(Restaurant).where(Restaurant.option == option)
        restaurants = session.exec(statement).all()
        # print(f"Getting {option} restaurants:")
        return [i for i in restaurants if i.option == option and print(i.restaurant)]


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
    # if not db_fn.exists():
    #     print("Creating database.")
    #     create_db_and_tables()

    #     if csv_fn.exists():
    #         with Session(engine) as session:
    #             with open(csv_fn) as f:
    #                 for line in f:
    #                     if line.startswith("restaurant"):
    #                         continue
    #                     restaurant, option = line.strip().split(",")
    #                     session.add(Restaurant(restaurant=restaurant, option=option))
    #             session.commit()
    #     else:
    #         with Session(engine) as session:
    #             session.add(Restaurant(restaurant="McDonald's", option="cheap"))
    #             session.add(Restaurant(restaurant="Taco John's", option="normal"))
    #             session.commit()

    #     print("Database created!")
    # else:
    #     print("Database already exists.")

    create_db_and_tables()

    print(get_all_restaurants())
    print(get_restaurants("normal"))


if __name__ == "__main__":
    main()
