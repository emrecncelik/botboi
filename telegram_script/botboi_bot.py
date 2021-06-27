import sys
import telebot
from decouple import config
from telegram_script import botboi_bridge


tgm_token = config("TELEGRAM_API_TOKEN")
group_user_id = config("TELEGRAM_GROUP_USERS").split(",")


bot = telebot.TeleBot(tgm_token, parse_mode=None)
bridge = botboi_bridge.dc_telegram_bridge(group_user_id, bot)


# TODO: Command 5adat will invoke dc bot, ask for online dc users, reply to telegram user
@bot.message_handler(commands=["online_dc"])
def get_online_dc_users(message):
    bot.reply_to(message, "Yalnız onu yanlış kodluyorsun kardeşim.")


argc = len(sys.argv)

# If script has called with parameters it means invoked by discord bot
# Use bridge to call function
if argc > 1:
    print(bridge.run_function(sys.argv))
    sys.stdout.flush()


# If not called with command line arguments
elif argc == 1:
    # Listen the server by long polling
    bot.polling()
