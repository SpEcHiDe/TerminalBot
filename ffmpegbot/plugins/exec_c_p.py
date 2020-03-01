from pyrogram import (
    Client,
    Filters
)

from ffmpegbot import (
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


@Client.on_message(Filters.command([EXEC_CMD_TRIGGER]) & Filters.chat(AUTH_USERS))
async def execution_cmd_t(client, message):
    status_message = await message.reply_text(PROCESS_RUNNING, quote=True)

    cmd = message.text.split(" ", maxsplit=1)[1].split(" ")

    await execute(
        cmd,
        lambda x: asyncio.get_event_loop().create_task(
            telegram_prog_m(
                f"<u>STDOUT</u>: \n<code>{x}</code>",
                status_message
            )
        ),
        lambda x: asyncio.get_event_loop().create_task(
            telegram_prog_m(
                f"<u>STDERR</u>: \n<code>{x}</code>",
                status_message
            )
        )
    )


# https://kevinmccarthy.org/2016/07/25/streaming-subprocess-stdin-and-stdout-with-asyncio-in-python/
async def _read_stream(stream, cb):
    while True:
        line = await stream.readline()
        if line:
            cb(line.decode())
        else:
            break


async def _stream_subprocess(cmd, stdout_cb, stderr_cb):
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    await asyncio.wait([
        _read_stream(process.stdout, stdout_cb),
        _read_stream(process.stderr, stderr_cb)
    ])
    return await process.wait()


async def execute(cmd, stdout_cb, stderr_cb):
    return await _stream_subprocess(
        cmd,
        stdout_cb,
        stderr_cb,
    )


async def telegram_prog_m(out_put, tg_message):
    try:
        current_message = out_put
        await tg_message.edit(current_message)
        await asyncio.sleep(DELAY_BETWEEN_EDITS)
    except:
        pass
