#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import telebot
import os
import pickle
from decouple import config
import sys
from inspect import signature

#Return the telegram discord dictionary
def get_tg_dc_dictionary(file_name):
    try:
        with open(assets_abs_path+file_name,"rb") as fp:
            return pickle.load(fp)
    except Exception as e:
        sys.stderr.write(e)
        return False
    
#Saves dictionary data with pickle
def save_tg_dc_dictionary(file_name):
    try:    
        with open(assets_abs_path+file_name,"wb") as fp:
            pickle.dump(telegram_dc_dictionary,fp)
            return True
            
    except Exception as e:
        sys.stderr.write(e)
        return False

#Get absolute path to assets
script_abs_path = os.path.dirname(__file__)
assets_relative_path = "assets/"
assets_abs_path = os.path.join(script_abs_path,assets_relative_path)

#Load local environment configuration
token = config("TELEGRAM_API_TOKEN")
#telegram_group_id = int(config("TELEGRAM_DEV_CHAT_ID"))
telegram_group_id = int(config("TELEGRAM_GROUP_ID"))
authorized_user_dc_id = config("AUTHORIZED_USER_DC_ID").split(",")
authorized_dev = config("AUTHORIZED_DEV_DC_ID").split(",")

#Dictionary for matching between discord and telegram
telegram_dc_filename = "telegram_dc_dictionary.pickle"
telegram_dc_dictionary = {}

#Load files
if os.path.exists(os.path.join(assets_abs_path,telegram_dc_filename)):    
    telegram_dc_dictionary = get_tg_dc_dictionary(telegram_dc_filename)

#Init telegram bot
bot = telebot.TeleBot(token,parse_mode=None)

#Connect telegram_id and discord_id in dictionary, save new pair to file
#Return True if added sucessfully, false if not
def add_discord_telegram_pair(telegram_username,dc_id,file_name=telegram_dc_filename):
    
    try:
        telegram_dc_dictionary[str(dc_id)] = str(telegram_username)
        result = save_tg_dc_dictionary(file_name)
        return result
    
    except Exception as e:
        sys.stderr.write(e)
        return False
    
def remove_discord_telegram_pair(dc_id,file_name=telegram_dc_filename):
    try:
        telegram_dc_dictionary.pop(str(dc_id))
        result = save_tg_dc_dictionary(file_name)
        return result
        
    except Exception as e:
        sys.stderr.write(e)
        return False
    

#TODO: Command 5adat will invoke dc bot, ask for online dc users, reply to telegram user
@bot.message_handler(commands=['online_dc'])
def get_online_dc_users(message):
	bot.reply_to(message, "Yalnız onu yanlış kodluyorsun kardeşim.")
    
    
def tag_message_id(tg_id,chat_id,message):
    bot.send_message(chat_id,message,parse_mode="MarkdownV2")
    

def call_for_5_adat(dc_user_id,dc_name,chat_id=telegram_group_id,local_dictionary=telegram_dc_dictionary):
    try:
        telegram_id = local_dictionary[str(dc_user_id)]
        message = "["+ dc_name+"]"+"(tg://user?id="+telegram_id+")"+", knights of round table await for the 5th adat \.\.\."
        tag_message_id(telegram_id,chat_id,message)
    except Exception as e:
        raise e
        
        
    
def get_function_index(function_name):
    try:
        for i in range(len(usable_methods_dc)):
            if str(usable_methods_dc[i].__name__) == str(function_name):
                return i
        
        return None
    
    except Exception as e:
        sys.stderr.write(e)
        return None
    
#Hardcoded due to security reasons. Only reachable methods out of the program
usable_methods_dc = [add_discord_telegram_pair,call_for_5_adat]
usable_methods_telegram = []

argc = len(sys.argv)

#If script has called with parameters it means invoked by discord bot
#Given arguments must be constructed as 
#function_to_invoke func_argument1 func_argument2 func_user_id
if(argc > 1):
    
    #Get the function given from the list
    function_index = get_function_index(sys.argv[1])
    
    #If not a callable function
    if(function_index < 0):
        print("Not a usable function. Try again, fail again, fail better.")
        sys.stdout.flush()
        quit()
    
    else: 
        #Get function parameters
        sig = signature(usable_methods_dc[function_index])
        func_param = [list(sig.parameters.keys())[i] for i in range(len(list(sig.parameters.keys()))) if "=" not in str(list(sig.parameters.values())[i])]
        
        #If not exact function argument count, see ya boy
        #-3(script name,function name,user that called function )
        if(argc-3 != len(func_param)):
            print("Man of many arguments, or few.")
            sys.stdout.flush()
            quit()
        
        #TODO: Give arguments dynamically regarding the number of parameters
        else:
            
            #TODO: Check authorization distinctively for dev and user
            #Check authorization
            if(sys.argv[-1] in authorized_user_dc_id):
                try:
                    #If given 2 argument
                    if(argc == 5):
                        usable_methods_dc[function_index](sys.argv[2],sys.argv[3])
                   
                    #Given 1 argument
                    elif(argc == 4):
                        usable_methods_dc[function_index](sys.argv[2])
                    
                    print("Function ran sucessfully")
                    sys.stdout.flush()
                    quit()
                
                except Exception as e:
                     print("Something gone terribly wrong. Try again, or maybe not")
                     sys.stdout.flush()
                     
                     sys.stderr.write(e)
                     quit()
                
            #Authorization failed
            else:
                print("Call me your manager")
                sys.stdout.flush()
                quit()
                

#If not called with command line arguments
elif(argc == 1):
    #Listen the server by long polling
    bot.polling()

    