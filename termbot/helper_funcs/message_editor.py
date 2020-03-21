#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Friendly Telegram (telegram userbot)
# Copyright (C) 2018-2019 GitHub/penn5

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
LOGGER = logging.getLogger(__name__)

from pyrogram import errors


class MessageEditor():
    def __init__(self, message, command):
        self.message = message
        self.command = command
        self.stdout = ""
        self.stdin = ""
        self.stderr = ""
        self.rc = None
        self.redraws = 0
        self.process = None
        self.state = 0

    async def update_stdout(self, stdout):
        self.stdout = stdout
        await self.redraw()

    async def update_stderr(self, stderr):
        self.stderr = stderr
        await self.redraw()

    async def update_stdin(self, stdin):
        self.stdin = stdin
        await self.redraw()

    async def redraw(self, skip_wait=False):
        text = "<b>Running command</b>: <code>{}<code>".format(self.command) + "\n"
        if self.rc is not None:
            text += "<b>process exited</b> with code <code>{}</code>".format(str(self.rc))
        if len(self.stdout) > 0:
            text += "\n\n" + "<b>STDOUT</b>:" + "\n"
            text += "<code>" + self.stdout[max(len(self.stdout) - 2048, 0):] + "</code>"
        if len(self.stderr) > 0:
            text += "\n\n" + "<b>STDERR</n>:" + "\n"
            text += "<code>" + self.stderr[max(len(self.stderr) - 1024, 0):] + "</code>"
        if len(self.stdin) > 0:
            text += "\n\n" + "<b>STDiN</n>:" + "\n"
            text += "<code>" + self.stdin[max(len(self.stdin) - 1024, 0):] + "</code>"
        try:
            await self.message.edit(text)
        except errors.MessageNotModified:
            pass
        except errors.MessageTooLong as e:
            LOGGER.error(e)
            LOGGER.error(text)
        # The message is never empty due to the template header

    async def cmd_ended(self, rc):
        self.rc = rc
        self.state = 4
        await self.redraw(True)

    def update_process(self, process):
        LOGGER.debug("got sproc obj %s", process)
        self.process = process
