#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


from ffmpegbot import (
    APP_ID,
    API_HASH,
    TG_BOT_TOKEN,
    TG_UPDATE_WORKERS_COUNT
)

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)


if __name__ == "__main__":
    plugins = dict(
        root="ffmpegbot/plugins"
    )
    app = pyrogram.Client(
        "FFMpegRoBot",
        api_id=APP_ID,
        api_hash=API_HASH,
        plugins=plugins,
        bot_token=TG_BOT_TOKEN,
        workers=TG_UPDATE_WORKERS_COUNT
    )
    #
    app.run()
