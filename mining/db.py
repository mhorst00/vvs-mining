from datetime import datetime
import functools
from sqlalchemy import create_engine, Integer, JSON, Column, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

EntityBase = declarative_base()

CURRENT_DATE = datetime.now().date()
ENGINE = create_engine(f"sqlite:///db{str(CURRENT_DATE)}.db", echo=True)
SESSION = sessionmaker(bind=ENGINE)()


class Trip(EntityBase):
    __tablename__ = "trips"
    id = Column(
        Integer, Sequence("trip_id_seq"), primary_key=True, nullable=False
    )
    information = Column(JSON, nullable=True)


# Create all tables derived from the EntityBase object
EntityBase.metadata.create_all(ENGINE)


def daily_db(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        new_date = datetime.now().date()
        if new_date > CURRENT_DATE:
            ENGINE = create_engine(
                f"sqlite:///db{str(new_date)}.db", echo=True
            )
            SESSION = sessionmaker(bind=ENGINE)()
            CURRENT_DAY = new_date
            EntityBase.metadata.create_all(ENGINE)
        return func(*args, **kwargs)

    return wrapper


@daily_db
def new_entry(trip):
    SESSION.add(trip)
    SESSION.commit()
    return True


# Declare a new row
first_item = Trip()
first_item.information = dict(a=1, b="foo", c=[1, 1, 2, 3, 5, 8, 13])

new_entry(first_item)


# Get all saved items from the database
for item in SESSION.query(Trip).all():
    print(type(item.information))
    # <class 'dict'>
    print(item.id, item.information)
