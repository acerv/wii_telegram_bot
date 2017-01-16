# Install & Run
To install bot dependences:
    
    $ sudo make install

In order to start the bot use the following command:

    $ python src/wii.py -t <your token> -q <quotes txt file>

Notice that the bot handles the quotes database as a `plain text file`.

# TODO 
* logging system
* store different quotes files for different chats (implement /start correctly)
* unittest with Travis (?)
