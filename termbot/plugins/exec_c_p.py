#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Telegram Terminal Bot
# CopyLeft AGPLv3 (C) 2020 The Authors

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
LOGGER = logging.getLogger(__name__)


from pyrogram import (
    Client,
    Filters,
    errors
)

from termbot import (
    AUTH_USERS,
    CHANGE_DIRECTORY_CTD,
    DELAY_BETWEEN_EDITS,
    EXEC_CMD_TRIGGER,
    MAX_MESSAGE_LENGTH,
    NO_CMD_RUNNING,
    PROCESS_RUNNING,
    SIG_KILL_CMD_TRIGGER,
    SIG_KILL_HELP_GNIRTS,
    TERMINATE_CMD_TRIGGER,
    TERMINATE_HELP_GNIRTS,
    TMP_DOWNLOAD_DIRECTORY,
    TYPE_CMD_TRIGGER,
    TYPE_HELP_GNIRTS,

    aktifperintah,
    inikerjasaatdirektori
)


import asyncio
import os


from termbot.helper_funcs.hash_msg import hash_msg
from termbot.helper_funcs.read_stream import read_stream
from termbot.helper_funcs.message_editor import MessageEditor


@Client.on_message(Filters.command([EXEC_CMD_TRIGGER]) & Filters.chat(AUTH_USERS))
async def execution_cmd_t(client, message):
    # send a message, use it to update the progress when required
    status_message = await message.reply_text(PROCESS_RUNNING, quote=True)
    # get the message from the triggered command
    cmd = message.text.split(" ", maxsplit=1)[1]

    process = await asyncio.create_subprocess_shell(
        cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=inikerjasaatdirektori
    )

    editor = MessageEditor(status_message, cmd)
    editor.update_process(process)

    aktifperintah[hash_msg(status_message)] = process
    await editor.redraw(True)
    await asyncio.gather(
        read_stream(
            editor.update_stdout,
            process.stdout,
            DELAY_BETWEEN_EDITS
        ),
        read_stream(
            editor.update_stderr,
            process.stderr,
            DELAY_BETWEEN_EDITS
        )
    )
    await editor.cmd_ended(await process.wait())
    del aktifperintah[hash_msg(status_message)]


@Client.on_message(Filters.command([TERMINATE_CMD_TRIGGER]) & Filters.chat(AUTH_USERS))
async def terminate_cmd_t(client, message):
    if message.reply_to_message is None:
        await message.reply_text(TERMINATE_HELP_GNIRTS, quote=True)
        return
    if hash_msg(message.reply_to_message) in aktifperintah:
        try:
            aktifperintah[hash_msg(message.reply_to_message)].terminate()
        except Exception:
            await message.reply_text("Could not Terminate!", quote=True)
        else:
            await message.reply_to_message.edit("Terminated!")
    else:
        await message.reply_text(NO_CMD_RUNNING, quote=True)


@Client.on_message(Filters.command([SIG_KILL_CMD_TRIGGER]) & Filters.chat(AUTH_USERS))
async def kill_cmd_t(client, message):
    if message.reply_to_message is None:
        await message.reply_text(SIG_KILL_HELP_GNIRTS, quote=True)
        return
    if hash_msg(message.reply_to_message) in aktifperintah:
        try:
            aktifperintah[hash_msg(message.reply_to_message)].kill()
        except Exception:
            await message.reply_text("Could not kill!", quote=True)
        else:
            await message.reply_to_message.edit("Killed!")
    else:
        await message.reply_text(NO_CMD_RUNNING, quote=True)


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
