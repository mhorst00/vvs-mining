import logging
import os
from discord import SyncWebhook, File
from datetime import datetime
from pathlib import Path

infoCount = 0
errorCount = 0
warningCount = 0

# webhook.send("<@&1020311126313009233> Hello there!") #Mention Role
# webhook.send("<#1020308171140628480> Hello there!") #Mention Channel
# k.send("<@> Hello there!") #Mention Person


WEBHOOK_LOGGING_URL = os.environ.get(
    "WEBHOOK_LOGGING_URL",
    "",
)
WEBHOOK_ERROR_URL = os.environ.get(
    "WEBHOOK_ERROR_URL",
    "",
)

WEBHOOK_ERROR_ENABLED = True
WEBHOOK_LOGGING_ENABLED = True

WEBHOOK_ERROR: SyncWebhook
WEBHOOK_LOGGING: SyncWebhook

LOG_FILENAME = f'/data/logs/mining_log {str(datetime.now()).replace(" ", "_")}.log'


def initialise():
    global WEBHOOK_ERROR
    global WEBHOOK_ERROR_ENABLED
    global WEBHOOK_LOGGING_ENABLED
    global WEBHOOK_LOGGING
    global LOG_FILENAME
    Path("/data/logs").mkdir(exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILENAME,
        filemode="a",
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )
    logger = logging.getLogger("mining_logger")
    # if url is not present disable the logging
    if WEBHOOK_ERROR_URL == "":
        logger.warning("WEBHOOK_ERROR_URL is not set, deactivating error logging")
        WEBHOOK_ERROR_ENABLED = False
    else:
        try:
            WEBHOOK_ERROR = SyncWebhook.from_url(WEBHOOK_ERROR_URL)
        except Exception as err:
            logger.warning(err)

    if WEBHOOK_LOGGING_URL == "":
        logger.warning("WEBHOOK_LOGGING_URL is not set, deactivating info logging")
        WEBHOOK_LOGGING_ENABLED = False
    else:
        try:
            WEBHOOK_LOGGING = SyncWebhook.from_url(WEBHOOK_LOGGING_URL)
        except Exception as err:
            logger.warning(err)


def finishLogging(numberOfTrips: int, numberOfBytes: int):
    global LOG_FILENAME
    global errorCount
    global warningCount
    global infoCount
    # send basic information about result
    if WEBHOOK_LOGGING_ENABLED:
        WEBHOOK_LOGGING.send("Import has finished")
        WEBHOOK_LOGGING.send("Number of trips: " + str(numberOfTrips))
        WEBHOOK_LOGGING.send("Size in bytes: " + str(numberOfBytes))
        message = f"There were {warningCount} Warnings and {infoCount} Infos"
        # send log file
        try:
            with open(file=LOG_FILENAME, mode="rb") as f:
                file = File(f)
        except Exception as err:
            logger = logging.getLogger("mining_logger")
            logger.warning(err)
        WEBHOOK_LOGGING.send(message, file=file)

    if WEBHOOK_ERROR_ENABLED:
        message = f"There were {errorCount} Errors"
        WEBHOOK_ERROR.send(message)


def info(message):
    global infoCount
    logger = logging.getLogger("mining_logger")
    logger.info(message)
    infoCount += 1


def warning(message):
    global warningCount
    logger = logging.getLogger("mining_logger")
    logger.warn(message)
    warningCount += 1


def error(message):
    global WEBHOOK_ERROR
    global errorCount
    logger = logging.getLogger("mining_logger")
    logger.exception(message)
    errorCount += 1
    if WEBHOOK_ERROR_ENABLED:
        WEBHOOK_ERROR.send(
            "<@&1020311126313009233> " + "ERROR: " + str(message),
        )
