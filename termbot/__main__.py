#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Telegram Terminal Bot
# CopyLeft AGPLv3 (C) 2020 The Authors
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


# First we need the asyncio library
import asyncio
import importlib

from termbot import (
    API_HASH,
    APP_ID,
    Client,
    LOGGER,
    TG_BOT_TOKEN,
    TG_UPDATE_WORKERS_COUNT
)

from termbot.plugins import ALL_MODULES

async def main():
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
    #
    await Client.run_until_disconnected()

if __name__ == '__main__':
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    # Then we need a loop to work with
    loop = asyncio.get_event_loop()
    # Then, we need to run the loop with a task
    loop.run_until_complete(main())