import logging
import os
from discord import SyncWebhook, File
from datetime import datetime
from pathlib import Path

infoList = []
warningList = []
errorList = []

# webhook.send("<@&1020311126313009233> Hello there!") #Mention Role
# webhook.send("<#1020308171140628480> Hello there!") #Mention Channel
# k.send("<@> Hello there!") #Mention Person


WEBHOOK_LOGGING_URL = os.environ.get("WEBHOOK_LOGGING_URL", "")
WEBHOOK_ERROR_URL = os.environ.get("WEBHOOK_ERROR_URL", "")

WEBHOOK_ERROR_ENABLED = True
WEBHOOK_LOGGING_ENABLED = True

FILE_LOGGING_ENABLED = False
FILE_ERROR_ENABLED = False

WEBHOOK_ERROR: SyncWebhook
WEBHOOK_LOGGING: SyncWebhook


def initialise():
    global WEBHOOK_ERROR
    global WEBHOOK_ERROR_ENABLED
    global FILE_ERROR_ENABLED
    global WEBHOOK_LOGGING_ENABLED
    global FILE_LOGGING_ENABLED
    global WEBHOOK_LOGGING
    Path("./logs").mkdir(exist_ok=True)
    # if url is not present disable the corresponding logging
    if WEBHOOK_ERROR_URL == "":
        logging.warning(
            "WEBHOOK_ERROR_URL is not set, deactivating error logging"
        )
        WEBHOOK_ERROR_ENABLED = False
        FILE_ERROR_ENABLED = True
    else:
        try:
            WEBHOOK_ERROR = SyncWebhook.from_url(WEBHOOK_ERROR_URL)
            FILE_ERROR_ENABLED = False
        except Exception as err:
            logging.warning(err)
            FILE_ERROR_ENABLED = True

    if WEBHOOK_LOGGING_URL == "":
        logging.warning(
            "WEBHOOK_LOGGING_URL is not set, deactivating info logging"
        )
        WEBHOOK_LOGGING_ENABLED = False
        FILE_LOGGING_ENABLED = True
    else:
        try:
            WEBHOOK_LOGGING = SyncWebhook.from_url(WEBHOOK_LOGGING_URL)
            FILE_LOGGING_ENABLED = False
        except Exception as err:
            logging.warning(err)
            FILE_LOGGING_ENABLED = True


def writeFile(filename: str, messages):
    currentDirectory = os.getcwd()
    os.chdir("logs")
    with open(filename, "w") as f:
        for message in messages:
            f.write("%s\n" % message)
    f.close()
    os.chdir(currentDirectory)


def readFileForWebhooks(filename: str):
    file = None
    currentDirectory = os.getcwd()
    os.chdir("logs")
    with open(file=filename, mode="rb") as f:
        file = File(f)
    os.chdir(currentDirectory)
    return file


def deleteFile(filename: str):
    currentDirectory = os.getcwd()
    os.chdir("logs")
    os.remove(filename)
    os.chdir(currentDirectory)


def finishLogging(numberOfTrips: int, numberOfBytes: int):
    global FILE_ERROR_ENABLED
    global FILE_LOGGING_ENABLED
    # send basic information about result
    if WEBHOOK_LOGGING_ENABLED:
        WEBHOOK_LOGGING.send("Import has finished")
        WEBHOOK_LOGGING.send("Number of trips: " + str(numberOfTrips))
        WEBHOOK_LOGGING.send("Size in bytes: " + str(numberOfBytes))

    currentTime = str(datetime.now()).replace(" ", "_")

    # send detailed logs
    if len(infoList) > 0:
        infoFn = "info_" + currentTime + ".txt"
        writeFile(infoFn, infoList)
        # send logs to Discord if enabled
        if WEBHOOK_LOGGING_ENABLED:
            message = "There were " + str(len(infoList)) + " Infos:"
            file = readFileForWebhooks(infoFn)
            WEBHOOK_LOGGING.send(message, file=file)
        # only keep file if webhook is not functioning
        if not FILE_LOGGING_ENABLED:
            deleteFile(infoFn)

    if len(warningList) > 0:
        warningFn = "warning_" + currentTime + ".txt"
        writeFile(warningFn, warningList)
        if WEBHOOK_LOGGING_ENABLED:
            message = "There were " + str(len(warningList)) + " Warnings:"
            file = readFileForWebhooks(warningFn)
            WEBHOOK_LOGGING.send(message, file=file)
        if not FILE_LOGGING_ENABLED:
            deleteFile(warningFn)

    if len(errorList) > 0:
        errorFn = "error_" + currentTime + ".txt"
        writeFile(errorFn, errorList)
        if WEBHOOK_ERROR_ENABLED:
            message = "There were " + str(len(errorList)) + " Errors:"
            file = readFileForWebhooks(errorFn)
            WEBHOOK_ERROR.send(message, file=file)
        if not FILE_ERROR_ENABLED:
            deleteFile(errorFn)


def info(message: str):
    logging.info(message)
    infoList.append(str(datetime.now()).replace(" ", "_") + ": " + message)
    # webhookLogging.send("INFO: " + message)


def warning(message: str):
    logging.warn(message)
    warningList.append(str(datetime.now()).replace(" ", "_") + ": " + message)
    # webhookLogging.send("WARNING: " + message)


def error(message: str):
    logging.error(message)
    errorList.append(str(datetime.now()).replace(" ", "_") + ": " + message)
