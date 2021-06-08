#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Telegram Terminal Bot
# CopyLeft AGPLv3 (C) 2020 The Authors
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from pyrogram import Client, filters

from termbot import (
    AUTH_USERS,
    HELP_STICKER
)


@Client.on_message(~filters.chat(AUTH_USERS))
async def not_auth_text(client, message):
    await message.reply_sticker(HELP_STICKER, quote=True)
    if message.chat.type != "private":
        await message.chat.leave()
