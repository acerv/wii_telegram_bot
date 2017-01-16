import sys
import time
import telebot
from quotes import Quotes

"""
$ python2.7 wii.py <token> <quotes file>

The Wii IRC bot rebuilt for Telegram.
"""
token = sys.argv[1] # get token from command-line
qfile = sys.argv[2] # get quotes file from command-line

bot = telebot.TeleBot(token)
quotes = Quotes(qfile)

commands = {  # command description used in the "help" command
    'help': 
        'Gives information about the available commands',
    'quote': 
        'Return a random quote if no quote number is specified',
    'quote_add': 
        'Add a quote',
    'quote_rm':
        'Remove a quote',
    'quote_amount':
        'Show the amount of added quotes',
    'quote_last':
        'Show the last added quote'
}

def print_quote(message, num, quote):
    bot.reply_to(message, 'Quote #'+str(num)+': '+quote)

def print_message(message, msg):
    bot.reply_to(message, msg)

def print_error(message, error):
    print_message(message, error)

@bot.message_handler(commands=['quote'])
def command_quote(message):
    arg = message.text.replace('/quote', '')
    quotenum = 0
    text = ''

    if not arg:
        text, quotenum = quotes.random_read()
    elif arg.isdigit():
        quotenum = int(arg)
        tot_quotes = quotes.num_of_quotes()
        if quotenum > 0 and quotenum <= tot_quotes:
            text = quotes.read(quotenum)

    if not text:
        print_error(message, 'Quote not found')
    else:
        print_quote(message, quotenum, text)

@bot.message_handler(commands=['quote_amount'])
def command_quote_amount(message): 
    lastquotenum = quotes.num_of_quotes()
    print_message(message, str(lastquotenum) + ' total added quotes')

@bot.message_handler(commands=['quote_last'])
def command_quote_last(message): 
    lastquotenum = quotes.num_of_quotes()
    qtext = quotes.read(lastquotenum)
    print_quote(message, lastquotenum, qtext)

@bot.message_handler(commands=['quote_add'])
def command_quote_add(message):
    strsplit = message.text.split(' ')

    if len(strsplit) <= 1:
        print_error(message, 'Command failed: quote text is empty')
    else:
        text = strsplit[1]
        quotes.save(text)
        quotenum = quotes.num_of_quotes()
        print_quote(message, quotenum, text)

@bot.message_handler(commands=['quote_rm'])
def command_quote_rm(message):
    strsplit = message.text.split(' ')

    if len(strsplit) > 1:
        quotenum = int(strsplit[1])
        tot_quotes = quotes.num_of_quotes()
        if quotenum > 0 and quotenum <= tot_quotes:
            quotes.remove(quotenum)
            print_message(message, 'Quote \''+str(quotenum)+'\' removed')
        else:
            print_error(message, 'Quote number is out-of-range [1-'+str(tot_quotes)+']')
    else:
        print_error(message, 'Quote number is not valid')

@bot.message_handler(commands=['start', 'help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"

    bot.send_message(cid, help_text)

bot.polling()
