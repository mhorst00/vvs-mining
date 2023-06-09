import functools
from datetime import datetime
from pathlib import Path

import sqlalchemy.exc
import vvspy
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        Sequence, String, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from utils import PATH

Path(f"{PATH}/db").mkdir(exist_ok=True)
CURRENT_DATE = datetime.now().date()
ENGINE = create_engine(f"sqlite:///{PATH}/db/{str(CURRENT_DATE)}.db")
SESSION = sessionmaker(bind=ENGINE)()
ENTITY_BASE = declarative_base()


class Departure(ENTITY_BASE):
    __tablename__ = "departures"
    data_id = Column(Integer, Sequence("dep_id_seq"), primary_key=True, nullable=False)
    stop_id = Column(String)
    platform = Column(String)
    platform_name = Column(String)
    stop_name = Column(String)
    name_wo = Column(String)
    datetime = Column(DateTime(timezone=False))
    real_datetime = Column(DateTime(timezone=False))
    delay = Column(Integer)
    servingline_key = Column(String)
    servingline_code = Column(String)
    servingline_number = Column(String)
    servingline_realtime = Column(Boolean)
    servingline_direction = Column(String)
    servingline_direction_from = Column(String)
    servingline_name = Column(String)
    servingline_train_num = Column(String)
    servingline_dest_id = Column(String)
    operator_id = Column(String)
    operator_name = Column(String)
    operator_public_code = Column(String)
    line_infos = relationship("LineInfo", back_populates="data_dep")
    stop_infos = relationship("StopInfo", back_populates="data_dep")


class LineInfo(ENTITY_BASE):
    __tablename__ = "line_infos"
    data_id = Column(
        Integer, Sequence("line_info_id_seq"), primary_key=True, nullable=False
    )
    data_dep = relationship("Departure", back_populates="line_infos")
    data_dep_id = Column(Integer, ForeignKey("departures.data_id"))
    content = Column(String)
    subtitle = Column(String)
    subject = Column(String)


class StopInfo(ENTITY_BASE):
    __tablename__ = "stop_infos"
    data_id = Column(
        Integer, Sequence("stop_info_id_seq"), primary_key=True, nullable=False
    )
    data_dep = relationship("Departure", back_populates="stop_infos")
    data_dep_id = Column(Integer, ForeignKey("departures.data_id"))
    content = Column(String)
    subtitle = Column(String)
    subject = Column(String)


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
            ENGINE = create_engine(f"sqlite:///{PATH}/db/{str(new_date)}.db")
            SESSION = sessionmaker(bind=ENGINE)()
            CURRENT_DATE = new_date
            ENTITY_BASE.metadata.create_all(ENGINE)
        return func(*args, **kwargs)

    return wrapper


def new_departure(departure: vvspy.obj.Departure):
    new_dep = Departure()
    new_dep.stop_id = str(departure.stop_id)
    new_dep.platform = str(departure.platform)
    new_dep.platform_name = str(departure.platform_name)
    new_dep.stop_name = str(departure.stop_name)
    new_dep.name_wo = str(departure.name_wo)
    new_dep.datetime = departure.datetime
    new_dep.real_datetime = departure.real_datetime
    new_dep.delay = int(departure.delay)
    new_dep.servingline_key = str(departure.serving_line.key)
    new_dep.servingline_code = str(departure.serving_line.code)
    new_dep.servingline_number = str(departure.serving_line.number)
    new_dep.servingline_realtime = bool(departure.serving_line.real_time)
    new_dep.servingline_direction = str(departure.serving_line.direction)
    new_dep.servingline_direction_from = str(departure.serving_line.direction_from)
    new_dep.servingline_name = str(departure.serving_line.name)
    if "trainNum" in departure.serving_line.raw:
        new_dep.servingline_train_num = str(departure.serving_line.raw["trainNum"])
    new_dep.operator_id = str(departure.operator.id)
    new_dep.operator_name = str(departure.operator.name)
    new_dep.operator_public_code = str(departure.operator.public_code)
    if isinstance(departure.stop_infos, list):
        stop_info_list = []
        for stop_info in departure.stop_infos:
            new_stop_info = StopInfo()
            new_stop_info.content = str(stop_info["infoText"]["content"])
            new_stop_info.subtitle = str(stop_info["infoText"]["subtitle"])
            new_stop_info.subject = str(stop_info["infoText"]["subject"])
            stop_info_list.append(new_stop_info)
        new_dep.stop_infos = stop_info_list
    if isinstance(departure.line_infos, list):
        line_info_list = []
        for line_info in departure.line_infos:
            new_line_info = LineInfo()
            new_line_info.content = str(line_info["infoText"]["content"])
            new_line_info.subtitle = str(line_info["infoText"]["subtitle"])
            new_line_info.subject = str(line_info["infoText"]["subject"])
            line_info_list.append(new_line_info)
        new_dep.line_infos = line_info_list
    return new_dep


@daily_db
def new_entry(departure: vvspy.obj.Departure):
    try:
        SESSION.add(new_departure(departure))
        SESSION.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = str(e)
        return error


@daily_db
def new_entries(departures: list[vvspy.obj.Departure]):
    try:
        for i in departures:
            j = new_departure(i)
            if not j:
                continue
            SESSION.add(j)
        SESSION.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = str(e)
        return error


@daily_db
def del_entry(departure):
    try:
        SESSION.delete(departure)
        SESSION.flush()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = str(e)
        return error


@daily_db
def get_all_entries():
    try:
        return SESSION.query(Departure).all()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = str(e)
        return error


@daily_db
def get_first_entry() -> Departure | str:
    try:
        return SESSION.get(Departure, 1)
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = str(e)
        return error
