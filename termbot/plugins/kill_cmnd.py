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
    SIG_KILL_CMD_TRIGGER,
    SIG_KILL_HELP_GNIRTS,

    aktifperintah
)

from termbot.helper_funcs.hash_msg import hash_msg


@Client.on(events.NewMessage(chats=AUTH_USERS, pattern=SIG_KILL_CMD_TRIGGER))
async def kill_cmd_t(event):
    if event.reply_to_msg_id is None:
        await event.reply(SIG_KILL_HELP_GNIRTS)
        return
    reply_message = await event.get_reply_message()
    if hash_msg(reply_message) in aktifperintah:
        try:
            aktifperintah[hash_msg(reply_message)].process.kill()
        except Exception:
            await event.reply("Could not kill!")
        else:
            del aktifperintah[hash_msg(reply_message)]
            await reply_message.edit("Killed!")
    else:
        await event.reply(NO_CMD_RUNNING)
