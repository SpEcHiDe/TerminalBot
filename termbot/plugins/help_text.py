#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Telegram Terminal Bot
# CopyLeft AGPLv3 (C) 2020 The Authors
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from termbot import (
    Client
)
from telethon import events

from termbot import (
    AUTH_USERS,
    HELP_STICKER,
    START_CMD_TRIGGER
)


@Client.on(events.NewMessage(pattern=START_CMD_TRIGGER))
async def not_auth_text(event):
    await event.reply(str(event.chat_id), file=HELP_STICKER)
