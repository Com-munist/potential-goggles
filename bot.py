import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Define intents
intents = discord.Intents.default()
intents.messages = True  # Enable the messages intent
intents.message_content = True  # Enable privileged message content intent (required for reading messages)

# Discord bot setup
TOKEN = os.getenv('DISCORD_TOKEN')  # Replace with your actual bot token
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Run the bot
bot.run(TOKEN)

