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
    ARRAY,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

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
    isAdditional = Column(Boolean, nullable=False)
    interchanges = Column(Integer, nullable=False)
    legs = relationship("Leg", back_populates="data_trip")


class Leg(ENTITY_BASE):
    __tablename__ = "legs"
    data_id = Column(
        Integer, Sequence("leg_id_seq"), primary_key=True, nullable=False
    )
    data_trip_id = Column(Integer, ForeignKey("trips.data_id"))
    data_trip = relationship("Trip", back_populates="legs")
    duration = Column(Integer, nullable=False)
    isRealtimeControlled = Column(Boolean, nullable=False)
    realtimeStatus = Column(ARRAY(String), nullable=False)
    origin = relationship("Station", back_populates="data_origin")
    destination = relationship("Station", back_populates="data_destination")
    transportation_id = Column(String, nullable=False)
    transportation_name = Column(String, nullable=False)
    transportation_disassembledName = Column(String, nullable=False)
    transportation_number = Column(String, nullable=False)
    transportation_description = Column(String, nullable=False)
    transportation_product_id = Column(Integer, nullable=False)
    transportation_product_class = Column(Integer, nullable=False)
    transportation_product_name = Column(String, nullable=False)
    transportation_product_iconId = Column(Integer, nullable=False)
    transportation_operator_code = Column(String, nullable=False)
    transportation_operator_id = Column(String, nullable=False)
    transportation_operator_name = Column(String, nullable=False)
    transportation_destination_id = Column(String, nullable=False)
    transportation_destination_name = Column(String, nullable=False)
    transportation_destination_type = Column(String, nullable=False)
    transportation_properties_trainName = Column(String, nullable=False)
    transportation_properties_trainType = Column(String, nullable=False)
    transportation_properties_trainNumber = Column(String, nullable=False)
    transportation_properties_isROP = Column(Boolean, nullable=False)
    transportation_properties_tripCode = Column(Integer, nullable=False)
    transportation_properties_timetablePeriod = Column(String, nullable=False)
    transportation_properties_lineDisplay = Column(String, nullable=False)
    transportation_properties_globalId = Column(String, nullable=False)
    hints = relationship("Hint", back_populates="data_leg")
    stopSequence = relationship("Station", back_populates="data_stopSequence")
    infos = relationship("Info", back_populates="data_leg")
    pathDescriptions = relationship(
        "PathDescriptions", back_populates="data_pathDescriptions"
    )
    interchange_desc = Column(String, nullable=True)
    interchange_type = Column(Integer, nullable=True)
    interchange_coords = Column(ARRAY(Float, dimensions=2), nullable=True)
    properties_vehicleAccess = Column(ARRAY(String), nullable=False)
    properties_PlanWheelChairAccess = Column(String, nullable=True)


class Station(ENTITY_BASE):
    __tablename__ = "stations"
    data_id = Column(
        Integer, Sequence("station_id_seq"), primary_key=True, nullable=False
    )
    data_origin = relationship("Leg", back_populates="origin")
    data_origin_id = Column(Integer, ForeignKey("legs.data_id"), nullable=True)
    data_destination = relationship("Leg", back_populates="destination")
    data_destination_id = Column(
        Integer, ForeignKey("legs.data_id"), nullable=True
    )
    data_stopSequence = relationship("Leg", back_populates="stopSequence")
    data_stopSequence_id = Column(
        Integer, ForeignKey("legs.data_id"), nullable=True
    )
    isGlobalId = Column(Boolean, nullable=False)
    id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    disassembledName = Column(String, nullable=False)
    type = Column(String, nullable=False)
    pointType = Column(String, nullable=False)
    coord = Column(ARRAY(Float), nullable=False)
    niveau = Column(Integer, nullable=False)
    parent_isGlobalId = Column(Boolean, nullable=False)
    parent_id = Column(String, nullable=False)
    parent_name = Column(String, nullable=False)
    parent_disassembledName = Column(String, nullable=False)
    parent_type = Column(String, nullable=False)
    parent_parent_id = Column(String, nullable=False)
    parent_parent_name = Column(String, nullable=False)
    parent_parent_type = Column(String, nullable=False)
    parent_properties_stopId = Column(String, nullable=False)
    parent_coord = Column(ARRAY(Float), nullable=False)
    parent_niveau = Column(Integer, nullable=False)
    productClasses = Column(ARRAY(String), nullable=False)
    arrivalTimePlanned = Column(String, nullable=True)
    arrivalTimeEstimated = Column(String, nullable=True)
    departureTimePlanned = Column(String, nullable=True)
    departureTimeEstimated = Column(String, nullable=True)
    # properties_downloads does not contain usable data
    properties_areaNiveauDiva = Column(String, nullable=False)
    properties_stoppingPointPlanned = Column(String, nullable=False)
    properties_areaGid = Column(String, nullable=False)
    properties_area = Column(String, nullable=False)
    properties_platform = Column(String, nullable=False)
    properties_platformName = Column(String, nullable=False)


class PathDescriptions(ENTITY_BASE):
    __tablename__ = "pathDescriptions"
    data_id = Column(
        Integer, Sequence("path_desc_id_seq"), primary_key=True, nullable=False
    )
    data_pathDescriptions = relationship(
        "Leg", back_populates="pathDescriptions"
    )
    data_pathDescriptions_id = Column(Integer, ForeignKey("legs.data_id"))
    turnDirection = Column(String, nullable=False)
    manoeuvre = Column(String, nullable=False)
    name = Column(String, nullable=False)
    niveau = Column(Integer, nullable=False)
    coord = Column(ARRAY(Float), nullable=False)
    skyDirection = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    cumDuration = Column(Integer, nullable=False)
    distance = Column(Integer, nullable=False)
    cumDistance = Column(Integer, nullable=False)
    fromCoordsIndex = Column(Integer, nullable=False)
    toCoordsIndex = Column(Integer, nullable=False)
    properties_INDOOR_TYPE = Column(String, nullable=False)


class Info(ENTITY_BASE):
    __tablename__ = "infos"
    data_id = Column(
        Integer, Sequence("info_id_seq"), primary_key=True, nullable=False
    )
    data_leg = relationship("Leg", back_populates="infos")
    data_leg_id = Column(Integer, ForeignKey("legs.data_id"))
    priority = Column(String, nullable=False)
    id = Column(String, nullable=False)
    version = Column(String, nullable=False)
    type = Column(String, nullable=False)
    urlText = Column(String, nullable=False)
    url = Column(String, nullable=False)
    content = Column(String, nullable=False)
    subtitle = Column(String, nullable=False)
    title = Column(String, nullable=False)
    properties_publisher = Column(String, nullable=False)
    properties_infoType = Column(String, nullable=False)
    properties_timetableChange = Column(String, nullable=False)
    properties_htmlText = Column(String, nullable=False)
    properties_smsText = Column(String, nullable=False)


class Hint(ENTITY_BASE):
    __tablename__ = "hints"
    data_id = Column(
        Integer, Sequence("data_id"), primary_key=True, nullable=False
    )
    data_leg = relationship("Leg", back_populates="hints")
    data_leg_id = Column(Integer, ForeignKey("legs.data_id"))
    content = Column(String, nullable=False)
    providerCode = Column(String, nullable=False)
    type = Column(String, nullable=False)
    properties_subnet = Column(String, nullable=False)


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
        legs = list()
        for i in trip["legs"]:
            new_leg = Leg()
            new_leg.duration = int(i["duration"])
            new_leg.isRealtimeControlled = bool(i["isRealtimeControlled"])
            new_leg.realtimeStatus = i["realtimeStatus"]

            new_origin = Station()
            new_origin.isGlobalId = bool(i["origin"]["isGlobalId"])
            new_origin.id = str(i["origin"]["id"])
            new_origin.name = str(i["origin"]["name"])
            new_origin.disassembledName = str(i["origin"]["disassembledName"])
            new_origin.type = str(i["origin"]["type"])
            new_origin.pointType = str(i["origin"]["pointType"])
            new_origin.coord = i["origin"]["coord"]
            new_origin.niveau = int(i["origin"]["niveau"])
            new_origin.parent_isGlobalId = bool(
                i["origin"]["parent"]["isGlobalId"]
            )
            new_origin.parent_id = str(i["origin"]["parent"]["id"])
            new_origin.parent_name = str(i["origin"]["parent"]["name"])
            new_origin.parent_disassembledName = str(
                i["origin"]["parent"]["disassembledName"]
            )
            new_origin.parent_type = str(i["origin"]["parent"]["type"])
            new_origin.parent_parent_id = str(
                i["origin"]["parent"]["parent"]["id"]
            )
            new_origin.parent_parent_name = str(
                i["origin"]["parent"]["parent"]["name"]
            )
            new_origin.parent_parent_type = str(
                i["origin"]["parent"]["parent"]["type"]
            )
            new_origin.parent_properties_stopId = str(
                i["origin"]["parent"]["properties"]["stopId"]
            )
            new_origin.parent_coord = i["origin"]["parent"]["coord"]
            new_origin.parent_niveau = int(i["origin"]["parent"]["niveau"])
            new_origin.productClasses = i["origin"]["productClasses"]
            new_origin.departureTimePlanned = str(
                i["origin"]["departureTimePlanned"]
            )
            new_origin.departureTimeEstimated = str(
                i["origin"]["departureTimeEstimated"]
            )
            new_origin.properties_areaNiveauDiva = str(
                i["origin"]["properties"]["AREA_NIVEAU_DIVA"]
            )
            new_origin.properties_stoppingPointPlanned = str(
                i["origin"]["properties"]["stoppingPointPlanned"]
            )
            new_origin.properties_areaGid = str(
                i["origin"]["properties"]["areaGid"]
            )
            new_origin.properties_area = str(i["origin"]["properties"]["area"])
            new_origin.properties_platform = str(
                i["origin"]["properties"]["platform"]
            )
            new_origin.properties_platformName = str(
                i["origin"]["properties"]["platformName"]
            )
            new_leg.origin = new_origin

            new_destination = Station()
            new_destination.isGlobalId = bool(i["origin"]["isGlobalId"])
            new_destination.id = str(i["origin"]["id"])
            new_destination.name = str(i["origin"]["name"])
            new_destination.disassembledName = str(
                i["origin"]["disassembledName"]
            )
            new_destination.type = str(i["origin"]["type"])
            new_destination.pointType = str(i["origin"]["pointType"])
            new_destination.coord = i["origin"]["coord"]
            new_destination.niveau = int(i["origin"]["niveau"])
            new_destination.parent_isGlobalId = bool(
                i["origin"]["parent"]["isGlobalId"]
            )
            new_destination.parent_id = str(i["origin"]["parent"]["id"])
            new_destination.parent_name = str(i["origin"]["parent"]["name"])
            new_destination.parent_disassembledName = str(
                i["origin"]["parent"]["disassembledName"]
            )
            new_destination.parent_type = str(i["origin"]["parent"]["type"])
            new_destination.parent_parent_id = str(
                i["origin"]["parent"]["parent"]["id"]
            )
            new_destination.parent_parent_name = str(
                i["origin"]["parent"]["parent"]["name"]
            )
            new_destination.parent_parent_type = str(
                i["origin"]["parent"]["parent"]["type"]
            )
            new_destination.parent_properties_stopId = str(
                i["origin"]["parent"]["properties"]["stopId"]
            )
            new_destination.parent_coord = i["origin"]["parent"]["coord"]
            new_destination.parent_niveau = int(
                i["origin"]["parent"]["niveau"]
            )
            new_destination.productClasses = i["origin"]["productClasses"]
            new_destination.arrivalTimePlanned = str(
                i["origin"]["arrivalTimePlanned"]
            )
            new_destination.arrivalTimeEstimated = str(
                i["origin"]["arrivalTimeEstimated"]
            )
            new_destination.properties_areaNiveauDiva = str(
                i["origin"]["properties"]["AREA_NIVEAU_DIVA"]
            )
            new_destination.properties_stoppingPointPlanned = str(
                i["origin"]["properties"]["stoppingPointPlanned"]
            )
            new_destination.properties_areaGid = str(
                i["origin"]["properties"]["areaGid"]
            )
            new_destination.properties_area = str(
                i["origin"]["properties"]["area"]
            )
            new_destination.properties_platform = str(
                i["origin"]["properties"]["platform"]
            )
            new_destination.properties_platformName = str(
                i["origin"]["properties"]["platformName"]
            )
            new_leg.destination = new_destination

            new_leg.transportation_id = str(i["transportation"]["id"])
            new_leg.transportation_name = str(i["transportation"]["name"])
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
            new_leg.transportation_operator_code = str(
                i["transportation"]["operator"]["code"]
            )
            new_leg.transportation_operator_id = str(
                i["transportation"]["operator"]["id"]
            )
            new_leg.transportation_operator_name = str(
                i["transportation"]["operator"]["name"]
            )
            new_leg.transportation_destination_id = str(
                i["transportation"]["destination"]["id"]
            )
            new_leg.transportation_destination_name = str(
                i["transportation"]["destination"]["name"]
            )
            new_leg.transportation_destination_type = str(
                i["transportation"]["destination"]["type"]
            )
            new_leg.transportation_properties_trainName = str(
                i["transportation"]["properties"]["trainName"]
            )
            new_leg.transportation_properties_trainType = str(
                i["transportation"]["properties"]["trainType"]
            )
            new_leg.transportation_properties_trainNumber = str(
                i["transportation"]["properties"]["trainNumber"]
            )
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
                    new_hint.properties_subnet = str(
                        hint["properties"]["subnet"]
                    )
                    hint_list.append(new_hint)
                new_leg.hints = hint_list

            if "stops" in i:
                stops = list()
                for stop in i["stopSequence"]:
                    new_stop = Station()
                    new_stop.isGlobalId = bool(stop["origin"]["isGlobalId"])
                    new_stop.id = str(stop["origin"]["id"])
                    new_stop.name = str(stop["origin"]["name"])
                    new_stop.disassembledName = str(
                        stop["origin"]["disassembledName"]
                    )
                    new_stop.type = str(stop["origin"]["type"])
                    new_stop.pointType = str(stop["origin"]["pointType"])
                    new_stop.coord = stop["origin"]["coord"]
                    new_stop.niveau = int(stop["origin"]["niveau"])
                    new_stop.parent_isGlobalId = bool(
                        stop["origin"]["parent"]["isGlobalId"]
                    )
                    new_stop.parent_id = str(stop["origin"]["parent"]["id"])
                    new_stop.parent_name = str(
                        stop["origin"]["parent"]["name"]
                    )
                    new_stop.parent_disassembledName = str(
                        stop["origin"]["parent"]["disassembledName"]
                    )
                    new_stop.parent_type = str(
                        stop["origin"]["parent"]["type"]
                    )
                    new_stop.parent_parent_id = str(
                        stop["origin"]["parent"]["parent"]["id"]
                    )
                    new_stop.parent_parent_name = str(
                        stop["origin"]["parent"]["parent"]["name"]
                    )
                    new_stop.parent_parent_type = str(
                        stop["origin"]["parent"]["parent"]["type"]
                    )
                    new_stop.parent_properties_stopId = str(
                        stop["origin"]["parent"]["properties"]["stopId"]
                    )
                    new_stop.parent_coord = stop["origin"]["parent"]["coord"]
                    new_stop.parent_niveau = int(
                        stop["origin"]["parent"]["niveau"]
                    )
                    new_stop.productClasses = stop["origin"]["productClasses"]
                    if "departureTimePlanned" in stop["origin"]:
                        new_stop.departureTimePlanned = str(
                            stop["origin"]["departureTimePlanned"]
                        )
                    if "departureTimeEstimated" in stop["origin"]:
                        new_stop.departureTimeEstimated = str(
                            stop["origin"]["departureTimeEstimated"]
                        )
                    if "arrivalTimePlanned" in stop["origin"]:
                        new_stop.arrivalTimePlanned = str(
                            stop["origin"]["arrivalTimePlanned"]
                        )
                    if "arrivalTimeEstimated" in stop["origin"]:
                        new_stop.arrivalTimeEstimated = str(
                            stop["origin"]["arrivalTimeEstimated"]
                        )
                    new_stop.properties_areaNiveauDiva = str(
                        stop["origin"]["properties"]["AREA_NIVEAU_DIVA"]
                    )
                    new_stop.properties_stoppingPointPlanned = str(
                        stop["origin"]["properties"]["stoppingPointPlanned"]
                    )
                    new_stop.properties_areaGid = str(
                        stop["origin"]["properties"]["areaGid"]
                    )
                    new_stop.properties_area = str(
                        stop["origin"]["properties"]["area"]
                    )
                    new_stop.properties_platform = str(
                        stop["origin"]["properties"]["platform"]
                    )
                    new_stop.properties_platformName = str(
                        stop["origin"]["properties"]["platformName"]
                    )
                    stops.append(new_stop)

                new_leg.stopSequence = stops

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
                new_leg.infos = info_list

            new_leg.properties_vehicleAccess = str(
                i["properties"]["vehicleAccess"]
            )
            new_leg.properties_PlanWheelChairAccess = str(
                i["properties"]["PlanWheelChairAccess"]
            )
            legs.append(new_leg)

        new_trip = Trip()
        new_trip.rating = int(trip["rating"])
        new_trip.isAdditional = bool(trip["isAdditional"])
        new_trip.interchanges = int(trip["interchanges"])
        new_trip.legs = legs

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
