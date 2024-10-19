import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()  # Load environment variables from .env file

# Define intents
intents = discord.Intents.default()
intents.messages = True  # Enable the messages intent
intents.message_content = True  # Enable privileged message content intent (required for reading messages)

# Discord bot setup
TOKEN = os.getenv('DISCORD_TOKEN')  # Replace with your actual bot token
CHANNEL_ID = int(os.getenv('DISCORD_ID'))
key = os.getenv('DISCORD_KEY')

bot = commands.Bot(command_prefix='!', intents=intents)

key = key.encode() # Encode the key so it can use by Fernet
# Create the Fernet cipher object
cipher = Fernet(key)

@bot.event
async def on_message(message):
    """Event handler that processes messages."""
     print(f"Received message: {message.content} from {message.author.name}")  # Debug logging
    if message.channel.id == CHANNEL_ID:
        encrypted_message = message.content
        try:
            # Decrypt the received message
            decrypted_message = cipher.decrypt(encrypted_message.encode()).decode('utf-8')
            print(f"Decrypted message: {decrypted_message}")
        except Exception as e:
            print(f"Failed to decrypt message: {e}")
        # Do not forget to process other commands/messages
        await bot.process_commands(message)
# Run the bot
bot.run(TOKEN)

