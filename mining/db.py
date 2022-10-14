from datetime import datetime
import functools
import sqlalchemy.exc
from sqlalchemy import create_engine, Integer, JSON, Column, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

CURRENT_DATE = datetime.now().date()
ENGINE = create_engine(f"sqlite:///db{str(CURRENT_DATE)}.db")
SESSION = sessionmaker(bind=ENGINE)()
ENTITY_BASE = declarative_base()


class Trip(ENTITY_BASE):
    __tablename__ = "trips"
    id = Column(
        Integer, Sequence("trip_id_seq"), primary_key=True, nullable=False
    )
    information = Column(JSON, nullable=True)


# Create all tables derived from the EntityBase object
ENTITY_BASE.metadata.create_all(ENGINE)


def daily_db(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global CURRENT_DATE
        global ENGINE
        global SESSION
        global ENTITY_BASE
        new_date = datetime.now().date()
        if new_date > CURRENT_DATE:
            ENGINE = create_engine(f"sqlite:///db{str(new_date)}.db")
            SESSION = sessionmaker(bind=ENGINE)()
            CURRENT_DATE = new_date
            ENTITY_BASE.metadata.create_all(ENGINE)
        return func(*args, **kwargs)

    return wrapper


@daily_db
def new_entry(trip):
    try:
        new_trip = Trip()
        new_trip.information = trip
        SESSION.add(new_trip)
        SESSION.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        return error


@daily_db
def new_entries(trips: list[dict]):
    try:
        for i in trips:
            new_trip = Trip()
            new_trip.information = i
            SESSION.add(new_trip)
        SESSION.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        return error


@daily_db
def del_entry(trip):
    try:
        SESSION.delete(trip)
        SESSION.flush()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        return error


@daily_db
def get_all_entries():
    try:
        return SESSION.query(Trip).all()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        return error


@daily_db
def get_first_entry() -> Trip:
    try:
        return SESSION.get(Trip, 1)
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        return error
