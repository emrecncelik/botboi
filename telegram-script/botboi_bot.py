#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import telebot
from decouple import config
import botboi_bridge
import sys
import pickle
import random

tgm_token = config("TELEGRAM_API_TOKEN")
group_user_id = config("TELEGRAM_GROUP_USERS").split(",")

bot = telebot.TeleBot(tgm_token,parse_mode=None)
bridge = botboi_bridge.dc_telegram_bridge(group_user_id,bot)



#TODO: Command 5adat will invoke dc bot, ask for online dc users, reply to telegram user
@bot.message_handler(commands=['online_dc'])
def get_online_dc_users(message):
	bot.reply_to(message, "Yalnız onu yanlış kodluyorsun kardeşim.")

@bot.message_handler(commands=['add_public_address'])
def add_monero_public_address(message):
    public_address_tgm_id_pair={}
    if(len(message.text) == 95 or 101 and " " not in message.text):
        public_address_tgm_id_pair[message.from_user.id] = message.text
        
    else:
        bot.reply_to(message,"Something wrong with address, check again champ.")


@bot.message_handler(commands=['roll_2'])
def roll_two_six_die(message):
    int_to_emoji = {1:u'1\uFE0F\u20E3',2:u'2\uFE0F\u20E3',3:u'3\uFE0F\u20E3',4:u'4\uFE0F\u20E3',5:u'5\uFE0F\u20E3',6:u'6\uFE0F\u20E3'}
    random1 = random.randrange(1,7)
    random2 = random.randrange(1,7)
    bot.reply_to(message, int_to_emoji[random1] + int_to_emoji[random2])
    if(random1==6 and random2==6):
        bot.send_message(message.chat.id,"You lucky bastard")
    
@bot.message_handler(commands=['roll_420'])
def roll_a_cigar(message):
    bot.reply_to(message, "🪣")
    
argc = len(sys.argv)

#If script has called with parameters it means invoked by discord bot
#Use bridge to call function
if(argc > 1):
    print(bridge.run_function(sys.argv))
    sys.stdout.flush()
    
#If not called with command line arguments
elif(argc == 1):
    #Listen the server by long polling
    bot.polling()
 