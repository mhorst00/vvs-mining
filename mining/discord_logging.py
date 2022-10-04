import logging
import os
from discord import SyncWebhook, File
from datetime import datetime

infoList = []
warningList = []
errorList = []

# webhook.send("<@&1020311126313009233> Hello there!") #Mention Role
# webhook.send("<#1020308171140628480> Hello there!") #Mention Channel
# k.send("<@> Hello there!") #Mention Person

WEBHOOK_LOGGING_URL = os.environ["WEBHOOK_LOGGING_URL"]
WEBHOOK_ERROR_URL = os.environ["WEBHOOK_ERROR_URL"]

webhookLogging = SyncWebhook.from_url(WEBHOOK_LOGGING_URL)
webhookError = SyncWebhook.from_url(WEBHOOK_ERROR_URL)


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


def finishLogging(numberOfTrips: int, numberOfBytes: int):
    webhookLogging.send("Import has finished")
    webhookLogging.send("Number of trips: " + str(numberOfTrips))
    webhookLogging.send("Size in bytes: " + str(numberOfBytes))

    sendMessages()


def sendMessages():
    currentTime = str(datetime.now()).replace(" ", "_")

    if len(infoList) > 0:
        infoFn = "info_" + currentTime + ".txt"
        writeFile(infoFn, infoList)
        message = "There were " + str(len(infoList)) + " Infos:"
        file = readFileForWebhooks(infoFn)
        webhookLogging.send(message, file=file)
    if len(warningList) > 0:
        warningFn = "warning_" + currentTime + ".txt"
        writeFile(warningFn, warningList)
        message = "There were " + str(len(warningList)) + " Warnings:"
        file = readFileForWebhooks(warningFn)
        webhookLogging.send(message, file=file)
    if len(errorList) > 0:
        errorFn = "error_" + currentTime + ".txt"
        writeFile(errorFn, errorList)
        message = "There were " + str(len(errorList)) + " Errors:"
        file = readFileForWebhooks(errorFn)
        webhookError.send(message, file=file)


def info(message: str):
    # logging.info(message)
    infoList.append(message)
    # webhookLogging.send("INFO: " + message)


def warning(message: str):
    # logging.warn(message)
    warningList.append(message)
    # webhookLogging.send("WARNING: " + message)


def error(message: str):
    # logging.error(message)
    errorList.append(message)
    webhookError.send(
        "<@&1020311126313009233> " + "ERROR: " + message,
    )
