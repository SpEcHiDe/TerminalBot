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
    HELP_STICKER,
    START_CMD_TRIGGER
)

from telegram.ext import (
    Filters, 
    CommandHandler, 
    run_async
)


@run_async
def not_auth_text(update, context):
    update.message.reply_sticker(
        HELP_STICKER,
        quote=True
    )
    if update.message.chat.type != "private":
        update.message.chat.leave()


dispatcher.add_handler(
    CommandHandler(
        START_CMD_TRIGGER, 
        not_auth_text, 
        filters=~Filters.chat(AUTH_USERS)
    )
)

