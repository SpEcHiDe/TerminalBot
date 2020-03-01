from pyrogram import (
    Client,
    Filters
)

from ffmpegbot import (
    AUTH_USERS,
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

    cmd = message.text.split(" ", maxsplit=1)[1]

    DELAY_BETWEEN_EDITS = 0.3
    PROCESS_RUN_TIME = 100

    start_time = time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "No Error"
    o = stdout.decode()
    if not o:
        o = "No Output"
    else:
        _o = o.split("\n")
        o = "`\n".join(_o)
    final_output = f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n\n**stderr:** \n`{e}`\n**Output:**\n{o}"

    if len(final_output) > MAX_MESSAGE_LENGTH:
        with open("exec.text", "w+", encoding="utf8") as out_file:
            out_file.write(str(final_output))
        await status_message.reply_document(
            document="eval.text",
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=reply_to_id
        )
        os.remove("exec.text")
        await status_message.delete()
    else:
        await status_message.edit(final_output)
