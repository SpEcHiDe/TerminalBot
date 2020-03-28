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
    TERMINATE_CMD_TRIGGER,
    TERMINATE_HELP_GNIRTS,

    aktifperintah
)

from termbot.helper_funcs.hash_msg import hash_msg

from telegram.ext import (
    Filters, 
    CommandHandler, 
    run_async
)


def terminate_cmd_t(update, context):
    if update.message.reply_to_message is None:
        update.message.reply_text(TERMINATE_HELP_GNIRTS)
        return
    reply_message = update.message.reply_to_message
    if hash_msg(reply_message) in aktifperintah:
        try:
            aktifperintah[hash_msg(reply_message)].process.terminate()
        except Exception:
            update.message.reply_text("Could not Terminate!")
        else:
            del aktifperintah[hash_msg(message.reply_to_message)]
            reply_message.edit("Terminated!")
    else:
        update.message.reply_text(NO_CMD_RUNNING)


dispatcher.add_handler(
    CommandHandler(
        TERMINATE_CMD_TRIGGER, 
        terminate_cmd_t, 
        filters=Filters.chat(AUTH_USERS)
    )
)