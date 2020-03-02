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
            "."
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
