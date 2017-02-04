# Copyright (C) 2017 Andrea Cervesato
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
import logging
import random
import telebot
import urlparse
import urllib
import os
import confighelper
from imgurpython import ImgurClient

################
# LOGGER SETUP #
################
logger = logging.getLogger('wiibot')
logger.setLevel(logging.DEBUG)

myhandler = logging.StreamHandler()  # writes to stderr
myformatter = logging.Formatter(fmt='%(levelname)s: %(message)s')
myhandler.setFormatter(myformatter)

logger.addHandler(myhandler)

################
# HELP STRINGS #
################
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
        'FTTTT FTTTT',
    'russia':
        'Why Russia is amazing',
    'startrek':
        'Star Trek gifs'
}

#################
# CONFIGURAITON #
#################
logger.debug('reading config.ini..')

config = confighelper.get_config()
config.read('config.ini')

client_id = config.get('imgur', 'client_id')
client_secret = config.get('imgur', 'client_secret')

######################
# BOT INITIALIZATION #
######################
logger.debug('initialize bot..')

token = config.get('telegram', 'token')
bot = telebot.TeleBot(token)

#############
# UTILITIES #
#############
def print_message(message, msg):
    bot.reply_to(message, msg)

def print_error(message, error):
    print_message(message, error)

def show_sticker(message, name):
    logger.debug('show_sticker: showing '+name+' sticker')

    try:
        sticker_path = '../data/'+name+'.webp'
        with open(sticker_path, 'rb') as stickers:
            bot.send_sticker(message.chat.id, stickers)

        logger.debug('show_sticker:'+name+' sticker shown')
    except Exception, ex:
        print_message(message, "%s" % ex)

def show_subreddit_gallery_img(m, gallery):
    logger.debug('show_subreddit_gallery: fetching image from imgur')

    try:
        logger.debug('show_subreddit_gallery: getting imgur images urls..')
        client = ImgurClient(client_id, client_secret)
        items = client.subreddit_gallery(
            gallery, 
            sort='time', 
            window='week', 
            page=0)
        item_num = random.randint(1, len(items))
        item = items[item_num]

        url = ''

        if item.animated:
            # !!! HACK !!! 
            url = item.gifv[:-1]
        else:
            url = item.link

        bot.send_message(m.chat.id, url)

        logger.debug('show_subreddit_gallery: image sent')
    except Exception, ex:
        print_message(m, "%s" % ex)
        logger.exception(ex)

####################
# COMMANDS SECTION #
####################
@bot.message_handler(commands=['help'])
def command_help(m):
    logger.debug('command_help: printing help message')
    
    try:
        help_text = "The following commands are available: \n"
        for key in commands:
            help_text += "/" + key + ": "
            help_text += commands[key] + "\n"

        print_message(m, help_text)

        logger.debug('command_help: help message printed')
    except Exception, ex:
        print_message(m, "%s" % ex)

@bot.message_handler(commands=['lamerda'])
def command_lamerda(m):
    show_sticker(m, 'lamerda')
     
@bot.message_handler(commands=['fap'])
def command_fap(m):
    show_sticker(m, 'fap')

@bot.message_handler(commands=['bycicle'])
def command_bycicle(m):
    show_sticker(m, 'bycicle')

@bot.message_handler(commands=['irc_quote'])
def command_irc_quote(m):
    logger.debug('command_irc_quote: reading the quotes file')

    try:
        with open('../data/quotes.txt', 'r') as fquotes:
            num_lines = sum(1 for line in fquotes)
            num_rands = random.randint(1, num_lines)

            logger.debug('command_irc_quote: to send quote #'+str(num_rands))

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
    except Exception, ex:
        print_message(m, "%s" % ex)

@bot.message_handler(commands=['ftttt'])
def command_ftttt(m):
    bot.send_message(m.chat.id, '@valedix https://i.imgur.com/3STgUHv.jpg')

@bot.message_handler(commands=['russia'])
def command_russia(m):
    show_subreddit_gallery_img(m, 'ANormalDayInRussia')

@bot.message_handler(commands=['startrek'])
def command_startrek(m):
    show_subreddit_gallery_img(m, 'startrekgifs')

###############
# BOT POLLING #
###############
logger.debug('start bot polling..')

try:
    bot.polling()
except Exception, ex:
    logger.exception(ex)
