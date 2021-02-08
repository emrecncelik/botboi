#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import telebot
import os
import pickle
from decouple import config
import sys
from inspect import signature

#Get absolute path to assets
script_abs_path = os.path.dirname(__file__)
assets_relative_path = "assets/"
assets_abs_path = os.path.join(script_abs_path,assets_relative_path)

#Load local environment configuration
token = config("TELEGRAM_API_TOKEN")
telegram_group_id = int(config("TELEGRAM_GROUP_ID"))
authorized_user_dc_id = config("AUTHORIZED_USER_DC_ID").split(",")

#Dictionary for matching between discord and telegram
telegram_dc_filename = "telegram_dc_dictionary.pickle"
telegram_dc_dictionary = {}

#Init telegram bot
bot = telebot.TeleBot(token,parse_mode=None)


#Return the telegram discord dictionary
def get_tg_dc_dictionary(file_name):
    with open(assets_abs_path+file_name,"rb") as fp:
        return pickle.load(fp)
    
#Saves dictionary data with pickle
def save_tg_dc_dictionary(file_name):
    try:    
        with open(assets_abs_path+file_name,"wb") as fp:
            pickle.dump(telegram_dc_dictionary,fp)
            return True
            
    except:
        return False


#Connect telegram_id and discord_id in dictionary, save new pair to file
#Return True if added sucessfully, false if not
def add_discord_telegram_pair(telegram_username,dc_id,file_name=telegram_dc_filename):
    
    try:
        telegram_dc_dictionary[dc_id] = telegram_username
        result = save_tg_dc_dictionary(file_name)
        return result
    
    except:
        return False
    

#TODO: Command 5adat will invoke dc bot, ask for online dc users, reply to telegram user
@bot.message_handler(commands=['online_dc'])
def get_online_dc_users(message):
	bot.reply_to(message, "Yalnız onu yanlış kodluyorsun kardeşim.")
    
@bot.message_handler(commands=['eurydice'])
def eurydice(message):
    bot.reply_to(message,"Eurydice'ın söylediği şarkı bağlamada yazılıp çalınmış.Vauv" )


#Tags the person(user_id) in the group(chat_id)
def tag_person_in_chat(user_name,chat_id):
    bot.send_message(chat_id,"@"+user_name)
    
#Ultimate call for 5 adat
def call_for_5_adat(dc_user_id,chat_id=telegram_group_id,telegram_dc_dictionary=telegram_dc_dictionary):
    #Convert given dc_id to telegram user_name
    tag_person_in_chat(telegram_dc_dictionary[dc_user_id],chat_id)
    bot.send_message(chat_id,"Knights of round table await for 5 adat...")
    
def get_function_index(function_name):
    try:
        for i in range(len(usable_methods_dc)):
            if str(usable_methods_dc[i].__name__) == str(function_name):
                return i
        
        return None
    
    except:
        return None
    
#Hardcoded due to security reasons. Only reachable methods out of the program
usable_methods_dc = [add_discord_telegram_pair,call_for_5_adat]
methods_for_telegram = []


#Load files
if os.path.exists(telegram_dc_filename):    
    telegram_dc_dictionary = get_tg_dc_dictionary(telegram_dc_filename)


argc = len(sys.argv)

#If script has called with parameters it means invoked by discord bot
#Given arguments must be constructed as 
#function_to_invoke func_argument1 func_argument2 func_user_id
if(argc > 1):
    
    #Get the function given from the list
    function_index = get_function_index(sys.argv[1])
    print("Function index:"+str(function_index))
    
    #If not a callable function
    if(function_index < 0):
        print("Not a usable function. Try again, fail again, fail better.")
        sys.stdout.flush()
    
    else: 
        #Get function parameters
        sig = signature(usable_methods_dc[function_index])
        func_param = [list(sig.parameters.keys())[i] for i in range(len(list(sig.parameters.keys()))) if "=" not in str(list(sig.parameters.values())[i])]
        
        #If not exact function argument count, see ya boy
        #-3(script name,function name,user that called function )
        if(argc-3 != len(func_param)):
            print("Man of many arguments, or few.")
            sys.stdout.flush()
        
        #TODO: Give arguments dynamically regarding the number of parameters
        else:
            
            #Check authorization
            if(sys.argv[-1] in authorized_user_dc_id):
            #try:
                #If given 2 argument
                if(argc == 5):
                    usable_methods_dc[function_index](sys.argv[2],sys.argv[3])
               
                #Given 1 argument
                elif(argc == 4):
                    usable_methods_dc[function_index](sys.argv[2])
                
                print("Function run sucessfully")
                sys.stdout.flush()
            
            #except:
                 #print("Something gone very teribly, function sucessfully failed")
                 #sys.stdout.flush()
                
            #Authorization failed
            else:
                print("Call me your manager")
                sys.stdout.flush()
    

#If not called with command line arguments
elif(argc == 1):
    #Listen the server by long polling
    bot.polling()

    