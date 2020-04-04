#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Telegram Terminal Bot
# CopyLeft AGPLv3 (C) 2020 The Authors
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import importlib

from termbot import (
    updater,
    LOGGER,
    PORT,
    TG_BOT_TOKEN,
    TG_UPDATE_WORKERS_COUNT,
    URL,
    WEBHOOK
)

from termbot.plugins import ALL_MODULES


IMPORTED = {}
for module_name in ALL_MODULES:
    imported_module = importlib.import_module("termbot.plugins." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__
    
    if not imported_module.__mod_name__.lower() in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")
    
LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))


if WEBHOOK:
    LOGGER.info("Using webhooks.")
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TG_BOT_TOKEN
    )
    # https://t.me/MarieOT/22915
    updater.bot.set_webhook(url=URL + TG_BOT_TOKEN)
else:
    LOGGER.info("Using long polling.")
    updater.start_polling(timeout=15, read_latency=4)

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()