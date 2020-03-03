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
logger = logging.getLogger(__name__)


from pyrogram import (
    Client,
    Filters,
    errors
)

from termbot import (
    AUTH_USERS,
    DELAY_BETWEEN_EDITS,
    EXEC_CMD_TRIGGER,
    MAX_MESSAGE_LENGTH,
    PROCESS_RUNNING,
    SIG_KILL_CMD_TRIGGER,
    SIG_KILL_HELP_GNIRTS,
    TERMINATE_CMD_TRIGGER,
    TERMINATE_HELP_GNIRTS,
    TMP_DOWNLOAD_DIRECTORY
)


import asyncio
import os
import time


# a dictionary to store the currently running commands
aktifperintah = {}
# a variable to store the current working directory
inikerjasaatdirektori = os.path.abspath(
    os.path.dirname(
        os.path.abspath(
            os.getcwd()
        )
    )
)
logger.info(inikerjasaatdirektori)


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

    aktifperintah[hash_msg(message)] = process
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
    del aktifperintah[hash_msg(message)]


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
        await message.reply_text("No command is running in that message.", quote=True)


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
        await message.reply_text("No command is running in that message.", quote=True)


#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 GitHub/penn5

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


def hash_msg(message):
    return str(message.chat.id) + "/" + str(message.message_id)


async def read_stream(func, stream, delay):
    last_task = None
    data = b""
    while True:
        dat = (await stream.read(1))
        if not dat:
            # EOF
            if last_task:
                # Send all pending data
                last_task.cancel()
                await func(data.decode("utf-8"))
                # If there is no last task there is inherently no data, so theres no point sending a blank string
            break
        data += dat
        if last_task:
            last_task.cancel()
        last_task = asyncio.ensure_future(sleep_for_task(func, data, delay))


async def sleep_for_task(func, data, delay):
    await asyncio.sleep(delay)
    await func(data.decode("utf-8"))


class MessageEditor():
    def __init__(self, message, command):
        self.message = message
        self.command = command
        self.stdout = ""
        self.stderr = ""
        self.rc = None
        self.redraws = 0

    async def update_stdout(self, stdout):
        self.stdout = stdout
        await self.redraw()

    async def update_stderr(self, stderr):
        self.stderr = stderr
        await self.redraw()

    async def redraw(self, skip_wait=False):
        text = "<b>Running command</b>: <code>{}<code>".format(self.command) + "\n"
        if self.rc is not None:
            text += "<b>process exited</b> with code <code>{}</code>".format(str(self.rc))
        text += "\n\n" + "<b>STDOUT</b>:" + "\n"
        text += "<code>" + self.stdout[max(len(self.stdout) - 2048, 0):] + "</code>"
        text += "\n\n" + "<b>STDERR</n>:" + "\n"
        text += "<code>" + self.stderr[max(len(self.stdout) - 1024, 0):] + "</code>"
        try:
            await self.message.edit(text)
        except errors.MessageNotModified:
            pass
        except errors.MessageTooLong as e:
            logger.error(e)
            logger.error(text)
        # The message is never empty due to the template header

    async def cmd_ended(self, rc):
        self.rc = rc
        self.state = 4
        await self.redraw(True)

    def update_process(self, process):
        pass
