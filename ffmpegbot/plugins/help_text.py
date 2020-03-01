from pyrogram import Client, Filters

from ffmpegbot import (
    HELP_STICKER,
    TMP_DOWNLOAD_DIRECTORY
)


@Client.on_message(Filters.command(["start"]))
async def start_text(client, message):
    await message.reply_sticker(HELP_STICKER, quote=True)
