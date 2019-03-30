[![Build Status](https://travis-ci.org/acerv/wii_telegram_bot.svg?branch=master)](https://travis-ci.org/acerv/wii_telegram_bot)

# Run
The bot application works with both python2 and python3.
In order to start wii bot use the following command:

    python src/wiibot.py

# Configure
To configure the bot, create inside `src` directory a file called `config.ini`,
containing bot's configuration, like following:

    [telegram]
    token = <your bot token>

    [imgur]
    client_id = <imgur client id>
    client_secret = <imgur client secret>

