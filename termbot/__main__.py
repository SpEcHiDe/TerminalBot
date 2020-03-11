#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Telegram Terminal Bot
# CopyLeft AGPLv3 (C) 2020 The Authors
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# the logging things
import logging

from pyrogram import Client

from termbot import (
    API_HASH,
    APP_ID,
    TG_BOT_TOKEN,
    TG_UPDATE_WORKERS_COUNT
)


logging.getLogger("pyrogram").setLevel(logging.WARNING)


if __name__ == "__main__":
    plugins = dict(
        root="termbot/plugins"
    )
    app = Client(
        "TermBot",
        api_id=APP_ID,
        api_hash=API_HASH,
        plugins=plugins,
        bot_token=TG_BOT_TOKEN,
        workers=TG_UPDATE_WORKERS_COUNT
    )
    #
    app.run()
