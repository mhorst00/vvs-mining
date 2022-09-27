import logging
import os
from time import sleep
from discord import SyncWebhook



# webhook.send("<@&1020311126313009233> Hello there!") #Mention Role
# webhook.send("<#1020308171140628480> Hello there!") #Mention Channel
# k.send("<@> Hello there!") #Mention Person

WEBHOOK_LOGGING_URL =os.environ['WEBHOOK_LOGGING_URL']
WEBHOOK_ERROR_URL = os.environ['WEBHOOK_ERROR_URL']

class DiscordLogger:
    def __init__(self):
        if WEBHOOK_LOGGING_URL != "":
            self.webhookLogging = SyncWebhook.from_url(WEBHOOK_LOGGING_URL)
        if WEBHOOK_ERROR_URL != "":
            self.webhookError = SyncWebhook.from_url(WEBHOOK_ERROR_URL)

    def info(self, message: str):
        logging.info(message)
        self.webhookLogging.send("INFO: " + message)

    def warning(self, message: str):
        logging.warn(message)
        self.webhookLogging.send("WARNING: " + message)

    def error(self, message: str):
        logging.error(message)
        self.webhookError.send(
            "<@&1020311126313009233> " + "ERROR: " + message,
        )


disclogger = DiscordLogger()
#disclogger.info("eine info message")
# disclogger.warn("eine warn message")
#disclogger.error("kekw")
