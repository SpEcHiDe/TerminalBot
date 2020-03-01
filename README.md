# FFMpegBot

A Telegram Bot based on [Pyrogram](https://github.com/pyrogram/pyrogram)

## installing

#### The Easy Way

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

#### The Legacy Way
Simply clone the repository and run the main file:

```sh
git clone https://github.com/SpEcHiDe/FFMpegBot.git
cd FFMpegBot
virtualenv -p /usr/bin/python3 venv
. ./venv/bin/activate
pip install -r requirements.txt
# <Create config.py with variables as given below>
python3 -m ffmpegbot
```


## Getting config.py values

An example `config.py` file could be:

**Not All of the variables are mandatory**

__The Bot should work by setting only these variables__

```python3
from ffmpegbot.sample_config import Config

class Development(Config):
  APP_ID = 6
  API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
  TG_BOT_TOKEN = "123456789:eb98ae0f7-Gm_6d4abfb49dc_9dc3eBaEBa"
  AUTH_USERS = [
    7351948
  ]
```


## [@SpEcHlDe](https://telegram.dog/ThankTelegram)

- Only four of the configuration / environment variables are mandatory.
- This is because of `pyrogram.errors.API_ID_PUBLISHED_FLOOD`
    - `APP_ID`:   You can get this value from https://my.telegram.org
    - `API_HASH`:   You can get this value from https://my.telegram.org
    - `TG_BOT_TOKEN`: You can create a bot using [@BotFather](https://telegram.dog/BotFather)
    - `AUTH_USERS`: space sperated IDs of users who are allowed to use the bot
    - `TG_UPDATE_WORKERS_COUNT`: Number of workers to use. `1` is the recommended amount see for yourself what works best!
- The bot should work without setting the non-mandatory environment variables.
- Please report any issues to the support group: [@SpEcHlDe](https://t.me/joinchat/FrAVvUjG4FDOyhR3b-TEJg)


## Credits, and Thanks to

* [Dan Tès](https://telegram.dog/haskell) for his [Pyrogram Library](https://github.com/pyrogram/pyrogram)
