#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Telegram Terminal Bot
# CopyLeft AGPLv3 (C) 2020 The Authors
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# First we need the asyncio library
import asyncio

from termbot import (
    dispatcher
)

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

from telegram.ext import (
    Filters, 
    CommandHandler, 
    run_async
)


async def exec_comnd_prc(cmd, status_message):        
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


@run_async
def execution_cmd_t(update, context):
    # send a message, use it to update the progress when required
    status_message = update.message.reply_text(PROCESS_RUNNING)
    # get the message from the triggered command
    cmd = update.message.text.split(" ", maxsplit=1)[1]

    # Then we need a loop to work with
    loop = asyncio.get_event_loop()

    # Then, we need to run the loop with a task
    loop.run_until_complete(exec_comnd_prc(cmd, status_message))


dispatcher.add_handler(
    CommandHandler(
        EXEC_CMD_TRIGGER, 
        execution_cmd_t, 
        filters=Filters.chat(AUTH_USERS)
    )
)

