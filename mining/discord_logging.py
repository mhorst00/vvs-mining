import logging
import os
from datetime import datetime
from pathlib import Path

from discord import File, SyncWebhook
from utils import PATH

infoCount = 0
warningCount = 0
errorCount = 0


# webhook.send("<@&1020311126313009233> Hello there!") #Mention Role
# webhook.send("<#1020308171140628480> Hello there!") #Mention Channel
# k.send("<@> Hello there!") #Mention Person


WEBHOOK_LOGGING_URL = os.environ.get(
    "WEBHOOK_LOGGING_URL",
    "",
)

WEBHOOK_LOGGING_ENABLED = True

WEBHOOK_LOGGING: SyncWebhook

LOG_FILENAME = f'{PATH}/logs/mining_log-{str(datetime.now()).replace(" ", "-")}.log'


def initialise():
    global WEBHOOK_LOGGING_ENABLED
    global WEBHOOK_LOGGING
    global LOG_FILENAME
    Path(f"{PATH}/logs").mkdir(exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILENAME,
        filemode="a",
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )
    logger = logging.getLogger("mining_logger")

    if WEBHOOK_LOGGING_URL == "":
        logger.warning("WEBHOOK_LOGGING_URL is not set, deactivating info logging")
        WEBHOOK_LOGGING_ENABLED = False
    else:
        try:
            WEBHOOK_LOGGING = SyncWebhook.from_url(WEBHOOK_LOGGING_URL)
        except Exception as err:
            logger.warning(err)


def finishLogging(numberOfDepartures: int):
    global LOG_FILENAME
    global WEBHOOK_LOGGING
    global WEBHOOK_LOGGING_ENABLED
    global errorCount
    global warningCount
    global infoCount
    # send basic information about result
    if WEBHOOK_LOGGING_ENABLED:
        messageList = ["Import has finished\n"]
        if errorCount != 0:
            messageList.extend(
                f"<@&1020311126313009233> There were {errorCount} Errors! \n"
            )
        messageList.extend("Number of Departures: " + str(numberOfDepartures) + "\n")
        messageList.extend(f"There were {warningCount} Warnings and {infoCount} Infos")
        message = "".join(messageList)

        # send log file
        try:
            with open(file=LOG_FILENAME, mode="rb") as f:
                file = File(f)
        except Exception as err:
            logger = logging.getLogger("mining_logger")
            logger.warning(err)
        WEBHOOK_LOGGING.send(message, file=file)


def info(message):
    global infoCount
    logger = logging.getLogger("mining_logger")
    logger.info(message)
    infoCount += 1


def warning(message):
    global warningCount
    logger = logging.getLogger("mining_logger")
    logger.warning(message)
    warningCount += 1


def error(message):
    global errorCount
    logger = logging.getLogger("mining_logger")
    logger.error(message)
    errorCount += 1
