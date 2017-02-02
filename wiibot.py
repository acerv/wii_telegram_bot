import sys
import logging
import random
import telebot

# setup logger
logger = logging.getLogger('wiibot')
logger.setLevel(logging.DEBUG)
myhandler = logging.StreamHandler()  # writes to stderr
myformatter = logging.Formatter(fmt='%(levelname)s: %(message)s')
myhandler.setFormatter(myformatter)
logger.addHandler(myhandler)

# put here the bot's token
TOKEN='<token here>'

# command description used in the "help" command
commands = {      
    'help': 
        'Show the available commands',
    'lamerda':
        'Everything is lamerda',
    'fap':
        'It\'s FAP time',
    'bycicle':
        'Byyyyyycicle Byyyyyycicle',
    'irc_quote':
        'Show a quote from the old IRC channel',
    'ftttt':
        'FTTTT FTTTT'
}

# initialize bot
bot = telebot.TeleBot(TOKEN)

#############
# UTILITIES #
#############
def print_message(message, msg):
    bot.reply_to(message, msg)

def print_error(message, error):
    print_message(message, error)

def show_sticker(name, cid):
    logger.debug('show_sticker: showing '+name+' sticker')

    sticker_path = 'data/'+name+'.webp'
    with open(sticker_path, 'rb') as stickers:
        bot.send_sticker(cid, stickers)

    logger.debug('show_sticker:'+name+' sticker shown')

####################
# COMMANDS SECTION #
####################
@bot.message_handler(commands=['help'])
def command_help(m):
    logger.debug('command_help: printing help message')
    
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"

    bot.send_message(cid, help_text)

    logger.debug('command_help: help message printed')

@bot.message_handler(commands=['lamerda'])
def command_lamerda(m):
    show_sticker('lamerda', m.chat.id)
     
@bot.message_handler(commands=['fap'])
def command_fap(m):
    show_sticker('fap', m.chat.id)

@bot.message_handler(commands=['bycicle'])
def command_bycicle(m):
    show_sticker('bycicle', m.chat.id)

@bot.message_handler(commands=['irc_quote'])
def command_irc_quote(m):
    logger.debug('command_irc_quote: reading the quotes file')

    with open('data/quotes.txt', 'r') as fquotes:
        num_lines = sum(1 for line in fquotes)
        num_rands = random.randint(1, num_lines)

        logger.debug('command_irc_quote: ready to send quote #'+str(num_rands))

        text = ''

        fquotes.seek(0)
        for i, line in enumerate(fquotes):
            if i == num_rands - 1:
                text = line
                break

        if not text:
            print_error(m, 'Quote not found')
        else:
            print_message(m, text)

    logger.debug('command_irc_quote: quote sent')

@bot.message_handler(commands=['ftttt'])
def command_ftttt(m):
    logger.debug('command_ftttt: sending picture')

    with open('data/ftttt.jpeg', 'rb') as fftttt:
        bot.send_photo(m.chat.id, fftttt)

    logger.debug('command_ftttt: picture sent')

# start listening
logger.debug('Start bot polling...')

bot.polling()
