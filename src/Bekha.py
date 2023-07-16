"""
    Contributors: Riley Bagwell, Diego Trujano
    Created:    6/18/2023
    Last Edit:  7/16/2023
"""

import Park
import ActivityRequest
import os
from dotenv import load_dotenv
from datetime import datetime
import telebot

version = "v1.3.1"  # Version number


def findDir(targetDir):
    """Find the target directory"""
    abs_path = os.path.abspath(__file__)  # Absolute path to the file
    current_dir = abs_path
    while current_dir[len(current_dir) - 13:] != targetDir:  # Find the BEKHA directory
        current_dir = os.path.dirname(current_dir)
        if current_dir == "C:\\":  # Stop an endless loop if the folder isn't found
            print('Directory "BekhaTelegram" not found in project.')
            return "C:"
    return os.path.join(current_dir, ".env")


def getTime():
    """Return the time of when this method was called"""
    time = datetime.now()  # Used for the timestamp
    return time.strftime("%H:%M:%S") + ' ' + str(time.date())


def getUsername(message):
    """Return the username of who sent the given message. If they don't have a username, return the phone # instead."""
    tempName = message.from_user.username
    if str(tempName) == "None":
        tempName = message.from_user.phone_number
    return tempName


# Set up time
bot_start_time = getTime()

# Bot setup
env_dir = findDir("BekhaTelegram")  # Find directory
print("Found .env in directory " + env_dir)
load_dotenv(dotenv_path=env_dir)  # Load .env file
print("Loaded .env file")
BOT_TOKEN = os.getenv("TELEGRAM_KEY")  # Grab bot token from .env
print("Bot token obtained")
bot = telebot.TeleBot(BOT_TOKEN)  # Create the bot
print("Bot is running. Start time: " + bot_start_time + "\n")


@bot.message_handler(commands=['start', 's', 'help', 'h', 'commands', 'com', 'comm'])
def command_help(message):
    """Display the help message"""
    print(f"Command 'help' triggered by {getUsername(message)} at {getTime()}")
    reply = "Kai\\! I'm Bekha\\. I can show you all the information from the park's establishments\\.\n" + \
            "All information is pulled from FourZ the moment you send a command\\.\n\n" + \
            "You can use the following /commands:\n" + \
            "*help*: Show this message \\('help', 'h', 'start', 's'\\)\n" + \
            "*activities*: Show all active activity info for the park \\('act', a'\\)\n" + \
            "*empty*: Show all empty activities \\('empty', 'e'\\)\n" + \
            "*version*: Show bot information \\('info', 'version', 'v'\\)"
    bot.reply_to(message, reply, parse_mode='MarkdownV2')
    print("End of command\n")


@bot.message_handler(commands=['activities', 'a', 'act', 'active'])
def command_activities(message):
    """Display all activity information"""
    print(f"Command 'activities' triggered by {getUsername(message)} at {getTime()}")
    bot.reply_to(message, "Hang tight, I'm looking up activity information for you! This may take up to 20 seconds...")
    # API requests
    print("Requesting from API...")
    park = Park.Park()  # Create park object
    actReq = ActivityRequest.ActivityRequest(park)  # Create ActivityRequest object for API request and parsing
    print("Data received")

    # Build the messages to return
    chat_id = message.chat.id
    reply = f"There are *{park.guestsInActivities}* kids in activities right now, which is *{park.kidsBusyPercentage()}%* of the kid population\n" + \
            f"There are *{park.activeEstablishments}* activities with kids currently in them\n" + \
            f"The current population is *{park.currentGuests}*, with *{park.currentKids}* minor attendees"
    bot.send_message(chat_id, reply, parse_mode='MarkdownV2')  # Reply first message

    # Check that there are active activities
    if len(park.activities) != 0:
        reply = "Active establishments:\n\n"
        for obj in park.activities:
            if obj.currentGuests > 0:
                reply += obj.__str__() + "\n"
    else:
        reply = "There are currently no activities with guests in them."

    # Attempt to send the message
    try:
        if len(reply) <= 4096:  # Send the message if it's under telegram's limit
            bot.send_message(chat_id, reply)
        else:  # Otherwise, split it into two messages
            bot.send_message(chat_id, reply[:4095])
            bot.send_message(chat_id, reply[4095:])
    except:
        print("ERROR in command_activities(): likely the response was too long.")
    print("End of command\n")


@bot.message_handler(commands=['empty', 'e', 'inactive'])
def command_empty(message):
    """Display the empty establishments with no guests in them"""
    print(f"Command 'empty' triggered by {getUsername(message)} at {getTime()}")
    bot.reply_to(message, "Hang tight, I'm looking up activity information for you! This may take up to 20 seconds...")
    print("Requesting from API...")
    # API requests
    park = Park.Park()  # Create park object
    print("Data received")

    # Build the message to return
    chat_id = message.chat.id
    actReq = ActivityRequest.ActivityRequest(park)  # Create ActivityRequest object for API request and parsing
    reply = "Empty establishments: \n\n"
    park.finalizeEmptyEstablishments()  # Change emptyEstablishments dictionary to array
    for obj in park.emptyEstablishments:
        reply += obj + "\n"

    # Attempt to send the message
    try:
        if len(reply) <= 4096:  # Send the message if it's under telegram's limit
            bot.send_message(chat_id, reply)
        else:  # Otherwise, split it into two messages
            bot.reply_to(chat_id, reply[:4095])
            bot.send_message(chat_id, reply[4095:])
    except:
        print("ERROR in command_activities(): likely the response was too long.")
    print("End of command\n")


@bot.message_handler(commands=['info', 'i', 'version', 'v'])
def command_info(message):
    """Display the bot information"""
    print(f"Command 'info' triggered by {getUsername(message)} at {getTime()}")
    reply = f"Bekha version {version}\n" + \
            f"Bot has been running since {bot_start_time}"
    bot.reply_to(message, reply)
    print("End of command\n")


bot.infinity_polling()  # Keep the bot running
