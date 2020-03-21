#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Telegram Terminal Bot
# CopyLeft AGPLv3 (C) 2020 The Authors
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio

from pyrogram import (
    Client,
    Filters
)

from termbot import (
    AUTH_USERS,
    DELAY_BETWEEN_EDITS,
    NO_CMD_RUNNING,
    TYPE_CMD_TRIGGER,
    TYPE_HELP_GNIRTS,

    aktifperintah
)

from termbot.helper_funcs.hash_msg import hash_msg
from termbot.helper_funcs.read_stream import read_stream


@Client.on_message(Filters.command([TYPE_CMD_TRIGGER]) & Filters.chat(AUTH_USERS))
async def terminate_cmd_t(client, message):
    if message.reply_to_message is None:
        await message.reply_text(TYPE_HELP_GNIRTS, quote=True)
        return
    if hash_msg(message.reply_to_message) in aktifperintah:
        # get the input from the triggered command
        passed_ip = message.text.split(" ", maxsplit=1)[1]
        #
        current_message_editor = aktifperintah[hash_msg(message.reply_to_message)]
        process = current_message_editor.process
        process.stdin.write(passed_ip.encode("UTF-8") + b"\r\n")
        # https://stackoverflow.com/a/163556/4723940
        # process.stdin.close()
        # await process.communicate()
        #
    else:
        await message.reply_text(NO_CMD_RUNNING, quote=True)
