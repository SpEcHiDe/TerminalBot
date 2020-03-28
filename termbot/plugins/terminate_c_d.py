#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Telegram Terminal Bot
# CopyLeft AGPLv3 (C) 2020 The Authors
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from termbot import (
    Client
)
from telethon import events

from termbot import (
    AUTH_USERS,
    NO_CMD_RUNNING,
    TERMINATE_CMD_TRIGGER,
    TERMINATE_HELP_GNIRTS,

    aktifperintah
)

from termbot.helper_funcs.hash_msg import hash_msg


@Client.on(events.NewMessage(chats=AUTH_USERS, pattern=TERMINATE_CMD_TRIGGER))
async def terminate_cmd_t(event):
    if event.reply_to_msg_id is None:
        await event.reply(TERMINATE_HELP_GNIRTS)
        return
    reply_message = await event.get_reply_message()
    if hash_msg(reply_message) in aktifperintah:
        try:
            aktifperintah[hash_msg(reply_message)].process.terminate()
        except Exception:
            await event.reply("Could not Terminate!")
        else:
            del aktifperintah[hash_msg(message.reply_to_message)]
            await reply_message.edit("Terminated!")
    else:
        await event.reply(NO_CMD_RUNNING)
