# TerminalBot

A Telegram Bot based on [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot)

## installing

#### The Easy Way

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

#### The Legacy Way
Simply clone the repository and run the main file:

```sh
git clone https://github.com/SpEcHiDe/TerminalBot.git
cd TerminalBot
virtualenv -p /usr/bin/python3 venv
. ./venv/bin/activate
git checkout PTB
pip install -r requirements.txt
# <Create config.py with variables as given below>
python3 -m termbot
```


## Getting config.py values

An example `config.py` file could be:

**Not All of the variables are mandatory**

__The Bot should work by setting only these variables__

```python3
from termbot.sample_config import Config

class Development(Config):
  TG_BOT_TOKEN = "123456789:eb98ae0f7-Gm_6d4abfb49dc_9dc3eBaEBa"
  AUTH_USERS = [
    7351948
  ]
```


## [@SpEcHlDe](https://telegram.dog/ThankTelegram)

- Only three of the configuration / environment variables are mandatory.
    - `TG_BOT_TOKEN`: You can create a bot using [@BotFather](https://telegram.dog/BotFather)
    - `AUTH_USERS`: space sperated IDs of users who are allowed to use the bot
    - `TG_UPDATE_WORKERS_COUNT`: Number of workers to use. `1` is the recommended amount see for yourself what works best!
- The bot should work without setting the non-mandatory environment variables.
- Please report any issues to the support group: [@SpEcHlDe](https://t.me/joinchat/FrAVvUjG4FDOyhR3b-TEJg)


## Credits, and Thanks to

* [PTB Authors](https://t.me/pythontelegrambotgroup) for their [Python Telegram Bot Library](https://github.com/python-telegram-bot/python-telegram-bot)
