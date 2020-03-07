#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Telegram Terminal Bot
# CopyLeft AGPLv3 (C) 2020 The Authors

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from pyrogram import (
    Client,
    Filters
)

from termbot import (
    AUTH_USERS,
    NO_CMD_RUNNING,
    TYPE_CMD_TRIGGER,
    TYPE_HELP_GNIRTS,

    aktifperintah
)

from termbot.helper_funcs.hash_msg import hash_msg


@Client.on_message(Filters.command([TYPE_CMD_TRIGGER]) & Filters.chat(AUTH_USERS))
async def type_cmd_t(client, message):
    if message.reply_to_message is None:
        await message.reply_text(TYPE_HELP_GNIRTS, quote=True)
        return
    if hash_msg(message.reply_to_message) in aktifperintah:
        running_proc = aktifperintah[hash_msg(message.reply_to_message)]
        # get the message from the triggered command
        additional_input = message.text.split(" ", maxsplit=1)[1]
        running_proc.stdin.write(additional_input.encode("UTF-8") + b"\n")
    else:
        await message.reply_text(NO_CMD_RUNNING, quote=True)
