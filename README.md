# Install
To install bot dependences:
    
    $ make install

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

    $ cd ./src && python wiibot.py

