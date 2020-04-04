#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Telegram Terminal Bot
# CopyLeft AGPLv3 (C) 2020 The Authors
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from termbot import (
    dispatcher
)

from termbot import (
    AUTH_USERS,
    NO_CMD_RUNNING,
    SIG_KILL_CMD_TRIGGER,
    SIG_KILL_HELP_GNIRTS,

    aktifperintah
)

from termbot.helper_funcs.hash_msg import hash_msg

from telegram.ext import (
    Filters, 
    CommandHandler, 
    run_async
)


@run_async
def kill_cmd_t(update, context):
    if update.message.reply_to_message is None:
        update.message.reply_text(
            SIG_KILL_HELP_GNIRTS,
            quote=True
        )
        return
    reply_message = update.message.reply_to_message
    if hash_msg(reply_message) in aktifperintah:
        try:
            aktifperintah[hash_msg(reply_message)].process.kill()
        except Exception:
            update.message.reply_text("Could not kill!", quote=True)
        else:
            del aktifperintah[hash_msg(reply_message)]
            reply_message.edit_text("Killed!")
    else:
        update.message.reply_text(NO_CMD_RUNNING, quote=True)


dispatcher.add_handler(
    CommandHandler(
        SIG_KILL_CMD_TRIGGER, 
        kill_cmd_t, 
        filters=Filters.chat(AUTH_USERS)
    )
)