import os
from dotenv import load_dotenv
from discord.ext import commands
import requests
import json
import discord

load_dotenv()

client = discord.Client(intents=discord.Intents.all())

# registering a command with $ prefix
client = commands.Bot(command_prefix="$", intents=discord.Intents.all())

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
    return quote

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

    # if message startswith hello, reply with hello 
    if user_message.startswith("hello"):
         await message.channel.send('hello')

    # list of sad words pre-created above
    # if any of the sad words are in the message, the bot will send a random inspirational quote
    if any(word in user_message for word in sad_words):
        await message.channel.send(get_quote()) 
    
    await client.process_commands(message)

    # if 'happy' in user_message or 'good' in user_message or 'excited' in user_message:
    #     await message.channel.send(random.choice(insults))

# returning arguments if command detected
@client.command()
async def test(ctx, arg):
    await ctx.send(arg)

# activating the bot
client.run(token)