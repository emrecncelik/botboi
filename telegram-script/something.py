#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pickle
from decouple import config
import sys
from inspect import signature

class dc_telegram_bridge():
    
    def __init__(self,tgm_group_user_ids):
        self.tgm_dev_chat_id = int(config("TELEGRAM_DEV_CHAT_ID"))
        self.tgm_group_id = int(config("TELEGRAM_GROUP_ID"))
        self.authorized_user = config("AUTHORIZED_USER_DC_ID").split(",")
        self.authorized_dev = config("AUTHORIZED_DEV_DC_ID").split(",")
        self.tgm_dc_id_filename = "telegram_dc_dictionary.pickle"
        self.tgm_group_user_ids = tgm_group_user_ids
    
        #Get absolute path to assets
        script_abs_path = os.path.dirname(__file__)
        assets_relative_path = "assets/"
        self.assets_abs_path = os.path.join(script_abs_path,assets_relative_path)
        
        #If pair pickle exists
        if(os.path.exists(self.tgm_dc_id_filename)):
            self.tgm_dc_id_pair_dict = self.__get_tgm_dc_dictionary(self.tgm_dc_id_filename)
       
        #If does not exist, init with empty array
        else:
            self.tgm_dc_id_dict = []
            
        
    def __is_dev_authorized(self,discord_id):
        if discord_id not in self.authorized_dev:
            return False
        else:
            return True
        
    def __is_user_authorized(self,discord_id):
        if discord_id not in self.authorized_user:
            return False
        else:
            return True
        

    def __get_tgm_dc_dictionary(self,file_name):
        try:
            with open(self.assets_abs_path+file_name,"rb") as fp:
                return pickle.load(fp)
        except Exception as e:
            sys.stderr.write(e)
            sys.stderr.write("Empty array returned")
            return []
        
    #Saves dictionary data to a file as pickle
    def __save_tgm_dc_dict(self,file_name):
        try:    
            with open(self.assets_abs_path+file_name,"wb") as fp:
                pickle.dump(self.tgm_dc_id_pair_dict,fp)
                return True
                
        except Exception as e:
            sys.stderr.write(e)
            return False
    
    #Add id pairs with given discord id, save the new dictionary config
    def add_tgm_dc_pair(self,tgm_id,dc_id):
        if not self.__is_dev_authorized(dc_id):
            print("Unauthorized acces")
            sys.stdout.flush()
            return False
        
        try:
            self.tgm_dc_id_pair_dict[str(dc_id)] = str(tgm_id)
            result = self.__save_tgm_dc_dict(self.tgm_dc_id_filename)
            return result
        
        except Exception as e:
            sys.stderr.write(e)
            return False
    
    #Remove id pairs with given discord id, save the new dictionary config
    def remove_tgm_dc_pair(self,dc_id):
        
        if not self.__is_dev_authorized(dc_id):
            print("Unauthorized access")
            sys.stdout.flush()
            return False
        
        try:
            self.tgm_dc_id_dict.pop(str(dc_id))
            result = self.__save_tgm_dc_dict(self.tgm_dc_id_filename)
            return result
            
        except Exception as e:
            sys.stderr.write(e)
            return False
    
    def call_for_5_adat(self,dc_user_id,dc_name,bot):
        try:
            tgm_id = self.tgm_dc_id_pair_dict[str(dc_user_id)]
            message = "["+ dc_name+"]"+"(tg://user?id="+tgm_id+")"+", knights of round table await for the 5th adat \.\.\."
            
            if tgm_id in self.tgm_group_user_ids:
                self.__tgm_send_message_markdown2(self.tgm_group_id,message,bot)
            
            else:    
                self.__tgm_send_message_markdown2(tgm_id,message,bot)
        
        except Exception as e:
            raise e
    

    def __send_message_markdown2(self,chat_id,message,bot):
        bot.send_message(chat_id,message,parse_mode="MarkdownV2")
        

            