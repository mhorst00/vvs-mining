from datetime import datetime
import functools
import sqlalchemy.exc
from sqlalchemy import (
    create_engine,
    Integer,
    Column,
    Sequence,
    Boolean,
    String,
    ForeignKey,
)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

import json

CURRENT_DATE = datetime.now().date()
ENGINE = create_engine(f"sqlite:///db{str(CURRENT_DATE)}.db")
SESSION = sessionmaker(bind=ENGINE)()
ENTITY_BASE = declarative_base()


class Trip(ENTITY_BASE):
    __tablename__ = "trips"
    data_id = Column(
        Integer, Sequence("trip_id_seq"), primary_key=True, nullable=False
    )
    rating = Column(Integer, nullable=False)
    isAdditional = Column(Boolean, nullable=True)
    interchanges = Column(Integer, nullable=True)
    legs = relationship("Leg", back_populates="data_trip")


class Leg(ENTITY_BASE):
    __tablename__ = "legs"
    data_id = Column(
        Integer, Sequence("leg_id_seq"), primary_key=True, nullable=False
    )
    data_trip_id = Column(Integer, ForeignKey("trips.data_id"))
    data_trip = relationship("Trip", back_populates="legs")
    duration = Column(Integer, nullable=True)
    isRealtimeControlled = Column(Boolean, nullable=True)
    realtimeStatus = Column(String, nullable=True)
    transportation_id = Column(String, nullable=True)
    transportation_name = Column(String, nullable=True)
    transportation_disassembledName = Column(String, nullable=True)
    transportation_number = Column(String, nullable=True)
    transportation_description = Column(String, nullable=True)
    transportation_product_id = Column(Integer, nullable=True)
    transportation_product_class = Column(Integer, nullable=True)
    transportation_product_name = Column(String, nullable=True)
    transportation_product_iconId = Column(Integer, nullable=True)
    transportation_operator_code = Column(String, nullable=True)
    transportation_operator_id = Column(String, nullable=True)
    transportation_operator_name = Column(String, nullable=True)
    transportation_destination_id = Column(String, nullable=True)
    transportation_destination_name = Column(String, nullable=True)
    transportation_destination_type = Column(String, nullable=True)
    transportation_properties_trainName = Column(String, nullable=True)
    transportation_properties_trainType = Column(String, nullable=True)
    transportation_properties_trainNumber = Column(String, nullable=True)
    transportation_properties_isROP = Column(Boolean, nullable=True)
    transportation_properties_tripCode = Column(Integer, nullable=True)
    transportation_properties_timetablePeriod = Column(String, nullable=True)
    transportation_properties_lineDisplay = Column(String, nullable=True)
    transportation_properties_globalId = Column(String, nullable=True)
    hints = relationship("Hint", back_populates="data_leg")
    stopSequence = relationship("Stop", back_populates="data_leg")
    infos = relationship("Info", back_populates="data_leg")
    pathDescriptions = relationship(
        "PathDescription", back_populates="data_pathDescription"
    )
    interchange_desc = Column(String, nullable=True)
    interchange_type = Column(Integer, nullable=True)
    interchange_coords = Column(String, nullable=True)
    properties_vehicleAccess = Column(String, nullable=True)
    properties_PlanWheelChairAccess = Column(String, nullable=True)


class Stop(ENTITY_BASE):
    __tablename__ = "stops"
    data_id = Column(
        Integer, Sequence("stops_id_seq"), primary_key=True, nullable=False
    )
    data_leg = relationship("Leg", back_populates="stopSequence")
    data_leg_id = Column(Integer, ForeignKey("legs.data_id"), nullable=False)
    isGlobalId = Column(Boolean, nullable=True)
    id = Column(String, nullable=True)
    name = Column(String, nullable=True)
    disassembledName = Column(String, nullable=True)
    type = Column(String, nullable=True)
    pointType = Column(String, nullable=True)
    coord = Column(String, nullable=True)
    niveau = Column(Integer, nullable=True)
    parent_isGlobalId = Column(Boolean, nullable=True)
    parent_id = Column(String, nullable=True)
    parent_name = Column(String, nullable=True)
    parent_disassembledName = Column(String, nullable=True)
    parent_type = Column(String, nullable=True)
    parent_parent_id = Column(String, nullable=True)
    parent_parent_name = Column(String, nullable=True)
    parent_parent_type = Column(String, nullable=True)
    parent_properties_stopId = Column(String, nullable=True)
    parent_coord = Column(String, nullable=True)
    parent_niveau = Column(Integer, nullable=True)
    productClasses = Column(String, nullable=True)
    arrivalTimePlanned = Column(String, nullable=True)
    arrivalTimeEstimated = Column(String, nullable=True)
    departureTimePlanned = Column(String, nullable=True)
    departureTimeEstimated = Column(String, nullable=True)
    # properties_downloads does not contain usable data
    properties_areaNiveauDiva = Column(String, nullable=True)
    properties_stoppingPointPlanned = Column(String, nullable=True)
    properties_areaGid = Column(String, nullable=True)
    properties_area = Column(String, nullable=True)
    properties_platform = Column(String, nullable=True)
    properties_platformName = Column(String, nullable=True)


class PathDescription(ENTITY_BASE):
    __tablename__ = "pathDescriptions"
    data_id = Column(
        Integer, Sequence("path_desc_id_seq"), primary_key=True, nullable=False
    )
    data_pathDescription = relationship(
        "Leg", back_populates="pathDescriptions"
    )
    data_pathDescription_id = Column(Integer, ForeignKey("legs.data_id"))
    turnDirection = Column(String, nullable=True)
    manoeuvre = Column(String, nullable=True)
    name = Column(String, nullable=True)
    niveau = Column(Integer, nullable=True)
    coord = Column(String, nullable=True)
    skyDirection = Column(Integer, nullable=True)
    duration = Column(Integer, nullable=True)
    cumDuration = Column(Integer, nullable=True)
    distance = Column(Integer, nullable=True)
    cumDistance = Column(Integer, nullable=True)
    fromCoordsIndex = Column(Integer, nullable=True)
    toCoordsIndex = Column(Integer, nullable=True)
    properties_INDOOR_TYPE = Column(String, nullable=True)


class Info(ENTITY_BASE):
    __tablename__ = "infos"
    data_id = Column(
        Integer, Sequence("info_id_seq"), primary_key=True, nullable=False
    )
    data_leg = relationship("Leg", back_populates="infos")
    data_leg_id = Column(Integer, ForeignKey("legs.data_id"))
    priority = Column(String, nullable=True)
    id = Column(String, nullable=True)
    version = Column(String, nullable=True)
    type = Column(String, nullable=True)
    urlText = Column(String, nullable=True)
    url = Column(String, nullable=True)
    content = Column(String, nullable=True)
    subtitle = Column(String, nullable=True)
    title = Column(String, nullable=True)
    properties_publisher = Column(String, nullable=True)
    properties_infoType = Column(String, nullable=True)
    properties_timetableChange = Column(String, nullable=True)
    properties_htmlText = Column(String, nullable=True)
    properties_smsText = Column(String, nullable=True)


class Hint(ENTITY_BASE):
    __tablename__ = "hints"
    data_id = Column(
        Integer, Sequence("data_id"), primary_key=True, nullable=False
    )
    data_leg = relationship("Leg", back_populates="hints")
    data_leg_id = Column(Integer, ForeignKey("legs.data_id"))
    content = Column(String, nullable=True)
    providerCode = Column(String, nullable=True)
    type = Column(String, nullable=True)
    properties_subnet = Column(String, nullable=True)


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


def new_trip(trip: dict):
    legs = list()
    for i in trip["legs"]:
        if not "trainType" in i["transportation"]["properties"]:
            # skip all other public transit methods except for trains
            return
        if "Bus" in str(i["transportation"]["properties"]["trainType"]):
            # skip possible bus routes on trip
            return
        new_leg = Leg()
        new_leg.duration = int(i["duration"])
        if "isRealtimeControlled" in i:
            new_leg.isRealtimeControlled = bool(i["isRealtimeControlled"])
        if "realtimeStatus" in i:
            new_leg.realtimeStatus = str(i["realtimeStatus"])

        if "transportation" in i:
            if "id" in i["transportation"]:
                new_leg.transportation_id = str(i["transportation"]["id"])
            new_leg.transportation_name = str(i["transportation"]["name"])
            if "disassembledName" in i["transportation"]:
                new_leg.transportation_disassembledName = str(
                    i["transportation"]["disassembledName"]
                )
            new_leg.transportation_number = str(i["transportation"]["number"])
            new_leg.transportation_description = str(
                i["transportation"]["description"]
            )
            new_leg.transportation_product_id = int(
                i["transportation"]["product"]["id"]
            )
            new_leg.transportation_product_class = int(
                i["transportation"]["product"]["class"]
            )
            new_leg.transportation_product_name = str(
                i["transportation"]["product"]["name"]
            )
            new_leg.transportation_product_iconId = int(
                i["transportation"]["product"]["iconId"]
            )
            if "code" in i["transportation"]["operator"]:
                new_leg.transportation_operator_code = str(
                    i["transportation"]["operator"]["code"]
                )
            new_leg.transportation_operator_id = str(
                i["transportation"]["operator"]["id"]
            )
            new_leg.transportation_operator_name = str(
                i["transportation"]["operator"]["name"]
            )
            if "id" in i["transportation"]["destination"]:
                new_leg.transportation_destination_id = str(
                    i["transportation"]["destination"]["id"]
                )
            new_leg.transportation_destination_name = str(
                i["transportation"]["destination"]["name"]
            )
            new_leg.transportation_destination_type = str(
                i["transportation"]["destination"]["type"]
            )
            if "trainName" in i["transportation"]["properties"]:
                new_leg.transportation_properties_trainName = str(
                    i["transportation"]["properties"]["trainName"]
                )
            new_leg.transportation_properties_trainType = str(
                i["transportation"]["properties"]["trainType"]
            )
            if "trainNumber" in i["transportation"]["properties"]:
                new_leg.transportation_properties_trainNumber = str(
                    i["transportation"]["properties"]["trainNumber"]
                )
            if "isROP" in i["transportation"]["properties"]:
                new_leg.transportation_properties_isROP = bool(
                    i["transportation"]["properties"]["isROP"]
                )
            new_leg.transportation_properties_tripCode = int(
                i["transportation"]["properties"]["tripCode"]
            )
            new_leg.transportation_properties_timetablePeriod = str(
                i["transportation"]["properties"]["timetablePeriod"]
            )
            new_leg.transportation_properties_lineDisplay = str(
                i["transportation"]["properties"]["lineDisplay"]
            )
            new_leg.transportation_properties_globalId = str(
                i["transportation"]["properties"]["globalId"]
            )

        if "hints" in i:
            hint_list = list()
            for hint in i["hints"]:
                new_hint = Hint()
                new_hint.content = str(hint["content"])
                new_hint.providerCode = str(hint["providerCode"])
                new_hint.type = str(hint["type"])
                new_hint.properties_subnet = str(hint["properties"]["subnet"])
                hint_list.append(new_hint)
            new_leg.hints = hint_list

        if "stopSequence" in i:
            stops = list()
            for stop in i["stopSequence"]:
                new_stop = Stop()
                new_stop.isGlobalId = bool(stop["isGlobalId"])
                new_stop.id = str(stop["id"])
                new_stop.name = str(stop["name"])
                if "disassembledName" in stop:
                    new_stop.disassembledName = str(stop["disassembledName"])
                if "type" in stop:
                    new_stop.type = str(stop["type"])
                if "pointType" in stop:
                    new_stop.pointType = str(stop["pointType"])
                new_stop.coord = str(stop["coord"])
                new_stop.niveau = int(stop["niveau"])
                if "isGlobalId" in stop["parent"]:
                    new_stop.parent_isGlobalId = bool(
                        stop["parent"]["isGlobalId"]
                    )
                new_stop.parent_id = str(stop["parent"]["id"])
                new_stop.parent_name = str(stop["parent"]["name"])
                if "disassembledName" in stop["parent"]:
                    new_stop.parent_disassembledName = str(
                        stop["parent"]["disassembledName"]
                    )
                new_stop.parent_type = str(stop["parent"]["type"])
                if "parent" in stop["parent"]:
                    new_stop.parent_parent_id = str(
                        stop["parent"]["parent"]["id"]
                    )
                    new_stop.parent_parent_name = str(
                        stop["parent"]["parent"]["name"]
                    )
                    new_stop.parent_parent_type = str(
                        stop["parent"]["parent"]["type"]
                    )
                if "properties" in stop["parent"]:
                    if "stopId" in stop["parent"]["properties"]:
                        new_stop.parent_properties_stopId = str(
                            stop["parent"]["properties"]["stopId"]
                        )
                if "coord" in stop["parent"]:
                    new_stop.parent_coord = str(stop["parent"]["coord"])
                if "niveau" in stop["parent"]:
                    new_stop.parent_niveau = int(stop["parent"]["niveau"])
                new_stop.productClasses = str(stop["productClasses"])
                if "departureTimePlanned" in stop:
                    new_stop.departureTimePlanned = str(
                        stop["departureTimePlanned"]
                    )
                if "departureTimeEstimated" in stop:
                    new_stop.departureTimeEstimated = str(
                        stop["departureTimeEstimated"]
                    )
                if "arrivalTimePlanned" in stop:
                    new_stop.arrivalTimePlanned = str(
                        stop["arrivalTimePlanned"]
                    )
                if "arrivalTimeEstimated" in stop:
                    new_stop.arrivalTimeEstimated = str(
                        stop["arrivalTimeEstimated"]
                    )
                new_stop.properties_areaNiveauDiva = str(
                    stop["properties"]["AREA_NIVEAU_DIVA"]
                )
                if "stoppingPointPlanned" in stop["properties"]:
                    new_stop.properties_stoppingPointPlanned = str(
                        stop["properties"]["stoppingPointPlanned"]
                    )
                new_stop.properties_areaGid = str(
                    stop["properties"]["areaGid"]
                )
                if "area" in stop["properties"]:
                    new_stop.properties_area = str(stop["properties"]["area"])
                if "platform" in stop["properties"]:
                    new_stop.properties_platform = str(
                        stop["properties"]["platform"]
                    )
                if "platformName" in stop["properties"]:
                    new_stop.properties_platformName = str(
                        stop["properties"]["platformName"]
                    )
                stops.append(new_stop)

            new_leg.stopSequence.extend(stops)

        if "infos" in i:
            info_list = list()
            for info in i["infos"]:
                new_info = Info()
                new_info.priority = str(info["priority"])
                new_info.id = str(info["id"])
                new_info.version = str(info["version"])
                new_info.type = str(info["type"])
                new_info.urlText = str(info["urlText"])
                new_info.url = str(info["url"])
                new_info.content = str(info["content"])
                new_info.subtitle = str(info["subtitle"])
                new_info.title = str(info["title"])
                new_info.properties_publisher = str(
                    info["properties"]["publisher"]
                )
                new_info.properties_infoType = str(
                    info["properties"]["infoType"]
                )
                if "timetableChange" in info["properties"]:
                    new_info.properties_timetableChange = str(
                        info["properties"]["timetableChange"]
                    )
                new_info.properties_htmlText = str(
                    info["properties"]["htmlText"]
                )
                new_info.properties_smsText = str(
                    info["properties"]["smsText"]
                )
                info_list.append(new_info)

            new_leg.infos.extend(info_list)

        if "pathDescriptions" in i:
            pathDescriptions = list()
            for desc in i["pathDescriptions"]:
                new_desc = PathDescription()
                new_desc.turnDirection = str(desc["turnDirection"])
                new_desc.manoeuvre = str(desc["manoeuvre"])
                new_desc.name = str(desc["name"])
                new_desc.niveau = int(desc["niveau"])
                new_desc.coord = str(desc["coord"])
                new_desc.skyDirection = int(desc["skyDirection"])
                new_desc.duration = int(desc["duration"])
                new_desc.cumDuration = int(desc["cumDuration"])
                new_desc.distance = int(desc["distance"])
                new_desc.cumDistance = int(desc["cumDistance"])
                new_desc.fromCoordsIndex = int(desc["fromCoordsIndex"])
                new_desc.toCoordsIndex = int(desc["toCoordsIndex"])
                if "properties" in desc:
                    new_desc.properties_INDOOR_TYPE = str(
                        desc["properties"]["INDOOR_TYPE"]
                    )

                pathDescriptions.append(new_desc)

            new_leg.pathDescriptions.extend(pathDescriptions)

        if "interchange" in i:
            new_leg.interchange_desc = str(i["interchange"]["desc"])
            new_leg.interchange_type = int(i["interchange"]["type"])
            new_leg.interchange_coords = str(i["interchange"]["coords"])

        if "properties" in i:
            if "vehicleAccess" in i["properties"]:
                new_leg.properties_vehicleAccess = str(
                    i["properties"]["vehicleAccess"]
                )
            if "PlanWheelChairAccess" in i["properties"]:
                new_leg.properties_PlanWheelChairAccess = str(
                    i["properties"]["PlanWheelChairAccess"]
                )
        legs.append(new_leg)

    new_trip = Trip()
    new_trip.rating = int(trip["rating"])
    new_trip.isAdditional = bool(trip["isAdditional"])
    new_trip.interchanges = int(trip["interchanges"])
    new_trip.legs = legs
    return new_trip


@daily_db
def new_entry(trip: dict):
    try:
        SESSION.add(new_trip(trip))
        SESSION.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = str(e)
        return error


@daily_db
def new_entries(trips: list[dict]):
    try:
        for i in trips:
            j = new_trip(i)
            if not j:
                continue
            SESSION.add(j)
        SESSION.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = str(e)
        return error


@daily_db
def del_entry(trip):
    try:
        SESSION.delete(trip)
        SESSION.flush()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = str(e)
        return error


@daily_db
def get_all_entries():
    try:
        return SESSION.query(Trip).all()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = str(e)
        return error


@daily_db
def get_first_entry() -> Trip:
    try:
        return SESSION.get(Trip, 1)
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = str(e)
        return error
