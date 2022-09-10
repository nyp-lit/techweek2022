import discord
import os
import random
from dotenv import load_dotenv
import requests
import json
from discord.ext import commands

load_dotenv()

client = discord.Client()
# might need to add the parameter: intents=discord.intents.all()
token = os.getenv('DISCORD_TOKEN')

# setting list of sad words
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]


# for API
# The get_quote() function uses the requests module to request data from the API URL. The API returns a random inspirational quote.
# json.loads() to convert the response from the API to JSON. 
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)

@client.event
async def on_ready():
	print("Logged in as a bot {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # get the message content & username
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    
    # if hello in message, reply with hi
    if 'hello' in user_message:
        await message.channel.send('hi')

    if message.content.startswith("$hello"):
        print('weeee')
    
    # list of sad words pre-created above
    # if any of the sad words are in the message, the bot will send a random inspirational quote    
    if any(word in user_message for word in sad_words):
        await message.channel.send(get_quote()) 
    
    # if 'happy' in user_message or 'good' in user_message or 'excited' in user_message:
    #     await message.channel.send(random.choice(insults))
   
# activating the bot
client.run(token)