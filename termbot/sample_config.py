#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Telegram Terminal Bot
# CopyLeft AGPLv3 (C) 2020 The Authors
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import os

class Config(object):
    LOGGER = True
    # 
    URL = os.environ.get("URL", None)
    PORT = int(os.environ.get("PORT", 5000))
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", None)
    # This is required for the plugins involving the file system.
    TMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./DOWNLOADS/")
    #
    TG_UPDATE_WORKERS_COUNT = int(os.environ.get("TG_UPDATE_WORKERS_COUNT", 1))
    # set to store users who are authorized to use the bot
    AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "").split())
    #
    # START command trigger
    START_CMD_TRIGGER = os.environ.get("START_CMD_TRIGGER", "start")
    # EVAL command trigger
    EVAL_CMD_TRIGGER = os.environ.get("EVAL_CMD_TRIGGER", "eval")
    # EXEC command trigger
    EXEC_CMD_TRIGGER = os.environ.get("EXEC_CMD_TRIGGER", "exec")
    # KILL command trigger
    SIG_KILL_CMD_TRIGGER = os.environ.get("SIG_KILL_CMD_TRIGGER", "kill")
    # TERMINATE command trigger
    TERMINATE_CMD_TRIGGER = os.environ.get("TERMINATE_CMD_TRIGGER", "terminate")
    #
    CHANGE_DIRECTORY_CTD = os.environ.get("CHANGE_DIRECTORY_CTD", ".")
    #
    DELAY_BETWEEN_EDITS = int(os.environ.get("DELAY_BETWEEN_EDITS", "2"))
    # TYPE command trigger
    TYPE_CMD_TRIGGER = os.environ.get("TYPE_CMD_TRIGGER", "type")


class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True
