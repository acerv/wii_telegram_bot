[![Build Status](https://travis-ci.org/acerv/wii_telegram_bot.svg?branch=master)](https://travis-ci.org/acerv/wii_telegram_bot)

# Python version
The bot is written using python version 2.7.12. If your system does not
provide it, you can use the `pyenv` package:

    pip install --no-cached-dir --egg pyenv

Follow the pyenv instructions to setup your environment, then run:

    pyenv install 2.7.12


# Install 
To install bot dependences:
    
    make install

# Configure
To configure the bot, create in the `src` directory a file called `config.ini`,
containing the bot's configuration, like following:

    [telegram]
    token = <your bot token>

    [imgur]
    client_id = <imgur client id>
    client_secret = <imgur client secret>

# Run
In order to start the bot use the following command:

    python src/wiibot.py

