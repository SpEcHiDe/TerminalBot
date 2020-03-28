#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Telegram Terminal Bot
# CopyLeft AGPLv3 (C) 2020 The Authors
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio

from termbot import (
    Client
)
from telethon import events

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


@Client.on(events.NewMessage(chats=AUTH_USERS, pattern=TYPE_CMD_TRIGGER))
async def type_cmd_t(event):
    if event.reply_to_msg_id is None:
        await event.reply(TYPE_HELP_GNIRTS)
        return
    reply_message = await event.get_reply_message()
    if hash_msg(reply_message) in aktifperintah:
        # get the input from the triggered command
        passed_ip = event.message.message.split(" ", maxsplit=1)[1]
        #
        current_message_editor = aktifperintah[hash_msg(reply_message)]
        process = current_message_editor.process
        process.stdin.write(passed_ip.encode("UTF-8") + b"\r\n")
        # https://stackoverflow.com/a/163556/4723940
        # process.stdin.close()
        # await process.communicate()
        #
    else:
        await event.reply(NO_CMD_RUNNING)
