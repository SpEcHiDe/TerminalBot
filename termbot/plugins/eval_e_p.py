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

from termbot import (
    dispatcher
)

from termbot import (
    AUTH_USERS,
    EVAL_CMD_TRIGGER,
    MAX_MESSAGE_LENGTH,
    PROCESS_RUNNING
)

from telegram.ext import (
    Filters, 
    CommandHandler, 
    run_async
)


@run_async
def evaluation_cmd_t(update, context):
    status_message = update.message.reply_text(PROCESS_RUNNING)

    cmd = update.message.text.split(" ", maxsplit=1)[1]

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        aexec(cmd, update, context)
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
        update.message.reply_document(
            document=open("eval.text", "rb"),
            caption=cmd
        )
        os.remove("eval.text")
        status_message.delete()
    else:
        status_message.edit(final_output)


def aexec(code, update, context):
    exec(
        f'def __aexec(update, context): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    return locals()['__aexec'](update, context)


dispatcher.add_handler(
    CommandHandler(
        EVAL_CMD_TRIGGER, 
        evaluation_cmd_t, 
        filters=Filters.chat(AUTH_USERS)
    )
)
