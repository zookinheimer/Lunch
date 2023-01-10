#!/usr/bin/env python3

from pathlib import Path
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional, Dict, List, Tuple


class Restaurant(SQLModel, table=True, tablename="lunch_list"):
    id: Optional[int] = Field(default=None, primary_key=True)
    restaurant: str
    option: str


db_fn = Path(__file__).parent / "test.db"
csv_fn = Path(__file__).parent / "restaurants.csv"

engine = create_engine(f"sqlite:///{db_fn.name}", echo=False)

if not db_fn.exists():
    print("Creating database.")
    SQLModel.metadata.create_all(engine)

    if csv_fn.exists():
        with Session(engine) as session:
            with open(csv_fn) as f:
                for line in f:
                    if line.startswith("restaurant"):
                        continue
                    restaurant, option = line.strip().split(",")
                    session.add(Restaurant(restaurant=restaurant, option=option))
            session.commit()
    else:
        with Session(engine) as session:
            session.add(Restaurant(restaurant="McDonald's", option="cheap"))
            session.add(Restaurant(restaurant="Taco John's", option="normal"))
            session.commit()

    print("Database created!")


def get_restaurants(option):
    with Session(engine) as session:
        statement = select(Restaurant).where(Restaurant.option == option)
        restaurants = session.exec(statement).all()
        print(f"Getting {option} restaurants:")
        [i for i in restaurants if i.option == option and print(i.restaurant)]


get_restaurants("normal")
