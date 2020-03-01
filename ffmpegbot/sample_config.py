#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import os

class Config(object):
    LOGGER = True
    # The Telegram API things
    APP_ID = int(os.environ.get("APP_ID", 12345))
    API_HASH = os.environ.get("API_HASH", None)
    # Get these values from my.telegram.org
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", None)
    # maximum message length in Telegram
    MAX_MESSAGE_LENGTH = 4096
    # This is required for the plugins involving the file system.
    TMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./DOWNLOADS/")
    #
    TG_UPDATE_WORKERS_COUNT = int(os.environ.get("TG_UPDATE_WORKERS_COUNT", 1))
    # set to store users who are authorized to use the bot
    AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "").split())
    #
    # EVAL command trigger
    EVAL_CMD_TRIGGER = os.environ.get("EVAL_CMD_TRIGGER", "eval")
    # EXEC command trigger
    EXEC_CMD_TRIGGER = os.environ.get("EXEC_CMD_TRIGGER", "exec")


class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True
