#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pickle
from decouple import config
import sys
from inspect import signature


class dc_telegram_bridge:
    def __init__(self, tgm_group_user_ids, bot):
        self.tgm_dev_chat_id = int(config("TELEGRAM_DEV_CHAT_ID"))
        self.tgm_group_id = int(config("TELEGRAM_GROUP_ID"))
        self.authorized_user = config("AUTHORIZED_USER_DC_ID").split(",")
        self.authorized_dev = config("AUTHORIZED_DEV_DC_ID").split(",")
        self.tgm_dc_id_filename = "tgm_dc_dict.pickle"
        self.tgm_group_user_ids = tgm_group_user_ids

        # TODO: Get all callable functions in a better way please
        self.usable_functions_dc = [
            self.add_tgm_dc_pair,
            self.remove_tgm_dc_pair,
            self.call_for_5_adat,
            self.run_function,
        ]

        # self.usable_functions_dc = [func for func in dir(dc_telegram_bridge) if callable(getattr(dc_telegram_bridge,func)) and not func.startswith("__")]
        self.bot = bot

        # Get absolute path to assets
        script_abs_path = os.path.dirname(__file__)
        assets_relative_path = "assets/"
        self.assets_abs_path = os.path.join(script_abs_path, assets_relative_path)

        # If pair pickle exists
        if os.path.exists(os.path.join(self.assets_abs_path, self.tgm_dc_id_filename)):
            self.tgm_dc_id_pair_dict = self.__get_tgm_dc_dictionary(
                self.tgm_dc_id_filename
            )

        # If does not exist, init with empty array
        else:
            self.tgm_dc_id_pair_dict = []

    def __is_dev_authorized(self, discord_id):
        if discord_id not in self.authorized_dev:
            return False
        else:
            return True

    def __is_user_authorized(self, discord_id):
        if discord_id not in self.authorized_user:
            return False
        else:
            return True

    def __get_tgm_dc_dictionary(self, file_name):
        try:
            with open(self.assets_abs_path + file_name, "rb") as fp:
                return pickle.load(fp)
        except:
            sys.stderr.write("Empty array returned")
            return []

    # Saves dictionary data to a file as pickle
    def __save_tgm_dc_dict(self, file_name):
        try:
            with open(self.assets_abs_path + file_name, "wb") as fp:
                pickle.dump(self.tgm_dc_id_pair_dict, fp)
                return True

        except:
            sys.stderr.write("Dictionary save failed due to unknown reasons.")
            return False

    def __tgm_send_message_markdown2(self, chat_id, message):
        self.bot.send_message(chat_id, message, parse_mode="MarkdownV2")

    def __get_function_index(self, function_name):
        try:
            for i in range(len(self.usable_functions_dc)):
                if str(self.usable_functions_dc[i].__name__) == str(function_name):
                    return i

            return None

        except:
            sys.stderr.write("Something gone wrong getting the function")
            return None

    # Add id pairs with given discord id, save the new dictionary config
    def add_tgm_dc_pair(self, tgm_id, dc_id, user_id):
        if not self.__is_dev_authorized(user_id):
            print("Unauthorized acces")
            sys.stdout.flush()
            return False

        try:
            self.tgm_dc_id_pair_dict[str(dc_id)] = str(tgm_id)
            result = self.__save_tgm_dc_dict(self.tgm_dc_id_filename)
            return result

        except:
            sys.stderr.write("Add pair failed")
            return False

    # Remove id pairs with given discord id, save the new dictionary config
    def remove_tgm_dc_pair(self, dc_id, user_id):

        if not self.__is_dev_authorized(user_id):
            print("Unauthorized access")
            sys.stdout.flush()
            return False

        try:
            self.tgm_dc_id_dict.pop(str(dc_id))
            result = self.__save_tgm_dc_dict(self.tgm_dc_id_filename)
            return result

        except:
            sys.stderr.write("Could not remove the pair")
            return False

    def call_for_5_adat(self, dc_user_id, dc_name, user_id):
        if not self.__is_user_authorized(user_id):
            print("Unauthorized access")
            sys.stdout.flush()
            return None

        try:
            tgm_id = self.tgm_dc_id_pair_dict[str(dc_user_id)]
            message = (
                "["
                + dc_name
                + "]"
                + "(tg://user?id="
                + tgm_id
                + ")"
                + ", knights of round table await for the 5th adat \.\.\."
            )

            if tgm_id in self.tgm_group_user_ids:
                self.__tgm_send_message_markdown2(self.tgm_group_id, message)

            else:
                self.__tgm_send_message_markdown2(tgm_id, message)

        except Exception as e:
            raise e

    def run_function(self, argv):
        argc = len(argv)

        # Get the function given from the list
        function_index = self.__get_function_index(argv[1])

        # If not a callable function
        if function_index < 0:
            return "Not a usable function. Try again, fail again, fail better."

        else:
            # Get function parameters
            sig = signature(self.usable_functions_dc[function_index])
            func_param = [
                list(sig.parameters.keys())[i]
                for i in range(len(list(sig.parameters.keys())))
                if "=" not in str(list(sig.parameters.values())[i])
            ]

            # If not exact function argument count, see ya boy
            # -2(script name,function name )
            if argc - 2 != len(func_param):

                return "Man of many arguments, or few:" + str(argc)

            # TODO: Give arguments dynamically regarding the number of parameters
            else:

                try:
                    self.usable_functions_dc[function_index](*argv[2:])
                    return "Function ran sucessfully"

                except:
                    return (
                        "Something gone terribly wrong. Dev check this out:"
                        + str(self.usable_functions_dc[function_index].__name__)
                        + ":"
                        + str(argv[2:])
                    )
