#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Telegram Terminal Bot
# CopyLeft AGPLv3 (C) 2020 The Authors
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import io
import os
import sys
import traceback

from pyrogram import (
    Client,
    Filters
)

from termbot import (
    AUTH_USERS,
    EVAL_CMD_TRIGGER,
    MAX_MESSAGE_LENGTH,
    PROCESS_RUNNING
)


@Client.on_message(Filters.command([EVAL_CMD_TRIGGER]) & Filters.chat(AUTH_USERS))
async def evaluation_cmd_t(client, message):
    status_message = await message.reply_text(PROCESS_RUNNING, quote=True)

    cmd = message.text.split(" ", maxsplit=1)[1]

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = "**EVAL**: ```{}```\n\n**OUTPUT**:\n```{}``` \n".format(cmd, evaluation.strip())

    if len(final_output) > MAX_MESSAGE_LENGTH:
        with open("eval.text", "w+", encoding="utf8") as out_file:
            out_file.write(str(final_output))
        await status_message.reply_document(
            document="eval.text",
            caption=cmd,
            disable_notification=True
        )
        os.remove("eval.text")
        await status_message.delete()
    else:
        await status_message.edit(final_output)


async def aexec(code, client, message):
    exec(
        f'async def __aexec(client, message): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    return await locals()['__aexec'](client, message)
