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
import logging.config
import random
import telebot
import yaml
import urlparse
import urllib
import os
import confighelper
import time
from imgurpython import ImgurClient

#####################
# WORKING DIRECTORY #
#####################
working_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(working_dir)

################
# LOGGER SETUP #
################
logger = logging.getLogger('wiibot')

with open('logging.yml', 'r') as fhandle:
    config = yaml.load(fhandle)
    logging.config.dictConfig(config)

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
        'Star Trek gifs',
    'cats':
        'Internet love cats',
    'dogs':
        'Internet love dogs',
    'nintendo':
        'Niiiiiintendo! Wahoo!',
    'mario':
        'It\'s me, Mario!',
    'doge':
        'Wow such a command!'
}

#################
# CONFIGURAITON #
#################
logger.info("reading configuration..")

config = confighelper.get_config()
config.read('config.ini')

client_id = config.get('imgur', 'client_id')
client_secret = config.get('imgur', 'client_secret')

######################
# BOT INITIALIZATION #
######################
logger.info("creating bot..")

token = config.get('telegram', 'token')
bot = telebot.TeleBot(token)

#############
# UTILITIES #
#############
def send_message(m, msg):
    logger.info("sending message..")
    logger.debug("msg=%s" % msg)
    logger.debug("m.chat.id=%s" % m.chat.id)
    logger.debug("m.chat.username=%s" % m.chat.username)

    try:
        bot.reply_to(m, msg)
    except Exception, ex:
        logger.exception(ex)

def send_error(m, error):
    send_message(m, error)

def send_sticker(m, stickerpath):
    logger.info("showing '%s' sticker.." % stickerpath)
    logger.debug("m.chat.id=%s" % m.chat.id)
    logger.debug("m.chat.username=%s" % m.chat.username)

    try:
        with open(stickerpath, 'rb') as sticker:
            bot.send_sticker(m.chat.id, sticker)
    except Exception, ex:
        send_message(m, "Runtime error")
        logger.exception(ex)

def send_subreddit_gallery_img(m, gallery):
    logger.info("showing image from subreddit gallery '%s'" % gallery)
    logger.debug("m.chat.id=%s" % m.chat.id)
    logger.debug("m.chat.username=%s" % m.chat.username)

    try:
        bot.send_chat_action(m.chat.id, 'upload_photo')

        client = ImgurClient(client_id, client_secret)
        items = client.subreddit_gallery(
            gallery,
            sort='time',
            window='week',
            page=0)

        item = random.choice(items)

        url = ''
        if item.is_album or not item.animated:
            url = item.link
        else:
            url = item.mp4

        logger.debug("image url='%s'" % str(url))

        bot.send_message(m.chat.id, url)
    except Exception, ex:
        send_message(m, "Runtime error")
        logger.exception(ex)

####################
# COMMANDS SECTION #
####################
@bot.message_handler(commands=['help'])
def command_help(m):
    logger.info("printing help message in chat..")
    logger.debug("m.chat.id=%s" % m.chat.id)
    logger.debug("m.chat.username=%s" % m.chat.username)

    try:
        help_text = "The following commands are available: \n"
        for key in commands:
            help_text += "/" + key + ": "
            help_text += commands[key] + "\n"

        send_message(m, help_text)
    except Exception, ex:
        send_message(m, "Runtime error")
        logger.exception(ex)

@bot.message_handler(commands=['lamerda'])
def command_lamerda(m):
    send_sticker(m, 'data/lamerda.webp')

@bot.message_handler(commands=['fap'])
def command_fap(m):
    send_sticker(m, 'data/fap.webp')

@bot.message_handler(commands=['bycicle'])
def command_bycicle(m):
    send_sticker(m, 'data/bycicle.webp')

@bot.message_handler(commands=['irc_quote'])
def command_irc_quote(m):
    logger.info("sending IRC quote..")
    logger.debug("m.chat.id=%s" % m.chat.id)
    logger.debug("m.chat.username=%s" % m.chat.username)

    try:
        with open('data/quotes.txt', 'r') as fquotes:
            num_lines = sum(1 for line in fquotes)
            num_rands = random.randint(1, num_lines)

            logger.debug("read quote #%s" % str(num_rands))

            text = ''

            fquotes.seek(0)
            for i, line in enumerate(fquotes):
                if i == num_rands - 1:
                    text = line
                    break

            if not text:
                send_error(m, 'Quote not found')
            else:
                send_message(m, text)
    except Exception, ex:
        send_message(m, "Runtime error")
        logger.exception(ex)

@bot.message_handler(commands=['ftttt'])
def command_ftttt(m):
    logger.info("sending ftttt url in chat..")
    logger.debug("m.chat.id=%s" % m.chat.id)
    logger.debug("m.chat.username=%s" % m.chat.username)

    try:
        bot.send_message(m.chat.id, '@valedix https://i.imgur.com/3STgUHv.jpg')
    except Exception, ex:
        send_message(m, "Runtime error")
        logger.exception(ex)

@bot.message_handler(commands=['russia'])
def command_russia(m):
    send_subreddit_gallery_img(m, 'ANormalDayInRussia')

@bot.message_handler(commands=['startrek'])
def command_startrek(m):
    send_subreddit_gallery_img(m, 'startrekgifs')

@bot.message_handler(commands=['cats'])
def command_cats(m):
    send_subreddit_gallery_img(m, 'catgifs')

@bot.message_handler(commands=['dogs'])
def command_dogs(m):
    send_subreddit_gallery_img(m, 'doggifs')

@bot.message_handler(commands=['nintendo'])
def command_nintendo(m):
    send_subreddit_gallery_img(m, 'nintendo')

@bot.message_handler(commands=['mario'])
def command_mario(m):
    send_subreddit_gallery_img(m, 'mario')

@bot.message_handler(commands=['doge'])
def command_doge(m):
    send_subreddit_gallery_img(m, 'doge')

###############
# BOT POLLING #
###############
logger.info('starting bot polling..')

while True:
    try:
        bot.polling(none_stop=True)
    except Exception, ex:
        logger.exception(ex)
        time.sleep(15)
