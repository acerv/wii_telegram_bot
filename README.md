# Install & Run
To install bot dependences:
    
    $ make install

In order to start the bot use the following command:

    $ python wiibot.py

# Configure
To configure the bot, create in the main directory a file called `config.ini`,
containing the bot's configuration, like following:

    [telegram]
    token = <your bot token>

    [imgur]
    client_id = <imgur client id>
    client_secret = <imgur client secret>
