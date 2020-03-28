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
    EXEC_CMD_TRIGGER,

    PROCESS_RUNNING,

    aktifperintah,
    inikerjasaatdirektori
)

from termbot.helper_funcs.hash_msg import hash_msg
from termbot.helper_funcs.read_stream import read_stream
from termbot.helper_funcs.message_editor import MessageEditor


@Client.on(events.NewMessage(chats=AUTH_USERS, pattern=EXEC_CMD_TRIGGER))
async def execution_cmd_t(event):
    # send a message, use it to update the progress when required
    status_message = await event.reply(PROCESS_RUNNING)
    # get the message from the triggered command
    cmd = event.message.message.split(" ", maxsplit=1)[1]

    process = await asyncio.create_subprocess_shell(
        cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=inikerjasaatdirektori
    )

    editor = MessageEditor(status_message, cmd)
    editor.update_process(process)

    aktifperintah[hash_msg(status_message)] = editor
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
