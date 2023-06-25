"""
    Main Contributor: Riley Bagwell
    Created:    6/18/2023
    Last Edit:  6/25/2023
"""

import Park
import ActivityRequest
import os
from dotenv import load_dotenv
from datetime import datetime
import telebot

version = "v0.1.0"  # Version number


def findDir(targetDir):
    abs_path = os.path.abspath(__file__)  # Absolute path to the file
    current_dir = abs_path
    while current_dir[len(current_dir) - 13:] != targetDir:  # Find the BEKHA directory
        current_dir = os.path.dirname(current_dir)
        if current_dir == "C:\\":  # Stop an endless loop if the folder isn't found
            print('Directory "BekhaTelegram" not found in project.')
            return "C:"
    return os.path.join(current_dir, ".env")


# Set up time
time = datetime.now()  # Used for the timestamp
start_time = time.strftime("%H:%M:%S") + ' ' + str(time.date())

# Bot config
print("Setting up bot")
load_dotenv(dotenv_path=findDir("BekhaTelegram"))  # Load .env file
BOT_TOKEN = os.getenv("TELEGRAM_KEY")  # Grab bot token from .env
bot = telebot.TeleBot(BOT_TOKEN)  # Create the bot


@bot.message_handler(commands=['start', 's', 'help', 'h', 'commands', 'com', 'comm'])
def command_help(message):
    """Display the help message"""
    reply = "Kai! I'm Bekha. I can show you all the information from the park's establishments!\n" + \
            "All information is pulled from FourZ the moment you send a command.\n\n" + \
            "You can use the following commands:\n" + \
            "help: Show this message (can also use 'start' or 'commands')\n" + \
            "activities: Show all active activity info for the park\n" + \
            "closed: Show all closed activities\n" + \
            "version: Show bot information"
    bot.reply_to(message, reply)


@bot.message_handler(commands=['activities', 'a', 'act', 'active'])
def command_activities(message):
    """Display all activity information"""
    # API requests
    park = Park.Park()  # Create park object
    actReq = ActivityRequest.ActivityRequest(park)  # Create ActivityRequest object for API request and parsing

    # Build the messages to return
    chat_id = message.chat.id
    reply = f"There are {park.guestsInActivities} kids in activities right now\n" + \
            f"There are {park.activeEstablishments} activities with kids currently in them\n" + \
            f"The current population is {park.currentGuests}, with {park.currentKids} minor attendees"
    bot.reply_to(message, reply)  # Reply first message

    reply = "Active establishments:\n\n"
    for obj in park.activities:
        if obj.currentGuests > 0:
            reply += obj.__str__() + "\n"

    # Attempt to send the message
    try:
        if len(reply) <= 4096:  # Send the message if it's under telegram's limit
            bot.send_message(chat_id, reply)
        else:  # Otherwise, split it into two messages
            bot.send_message(chat_id, reply[:4095])
            bot.send_message(chat_id, reply[4095:])
    except:
        print("ERROR in command_activities(): likely the response was too long.")


@bot.message_handler(commands=['closed', 'inactive'])
def command_closed(message):
    """Display the closed establishments with no guests in them"""
    # API requests
    park = Park.Park()  # Create park object

    # Build the message to return
    chat_id = message.chat.id
    actReq = ActivityRequest.ActivityRequest(park)  # Create ActivityRequest object for API request and parsing
    reply = "Empty establishments: \n\n"
    for key in park.emptyEstablishments:
        reply += key + "\n"

    # Attempt to send the message
    try:
        if len(reply) <= 4096:  # Send the message if it's under telegram's limit
            bot.send_message(chat_id, reply)
        else:  # Otherwise, split it into two messages
            bot.send_message(chat_id, reply[:4095])
            bot.send_message(chat_id, reply[4095:])
    except:
        print("ERROR in command_activities(): likely the response was too long.")


@bot.message_handler(commands=['info', 'i', 'version', 'v'])
def command_info(message):
    """Display the bot information"""
    reply = f"Bekha version {version}\n" + \
            f"Bot has been running since {start_time}"
    bot.reply_to(message, reply)


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    """Echo a message (unused)"""
    bot.reply_to(message, message.text)


print("Bot is running. Start time: " + start_time)
bot.infinity_polling()  # Keep the bot running
