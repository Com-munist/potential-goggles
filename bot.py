import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()  # Load environment variables from .env file

# Define intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # This is crucial for reading message content

# Discord bot setup
TOKEN = os.getenv('DISCORD_TOKEN_APPLE')
SOURCE_CHANNEL_ID = int(os.getenv('SOURCE_CHANNEL_ID'))
DEST_CHANNEL_ID = int(os.getenv('DEST_CHANNEL_ID'))
key = os.getenv('DISCORD_KEY').encode()  # Ensure this is set
cipher = Fernet(key)

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print(f"Source Channel ID: {SOURCE_CHANNEL_ID}")
    print("Bot is ready to read messages!")

@bot.event
async def on_message(message):
    """Event handler that processes messages."""
    print(f"Received message: {message.content} from {message.author.name} in channel {message.channel.id}")
    if message.channel.id == SOURCE_CHANNEL_ID:
        encrypted_message = message.content
        try:
            decrypted_message = cipher.decrypt(encrypted_message.encode()).decode('utf-8')
            print(f"Decrypted message: {decrypted_message}")

            dest_channel = bot.get_channel(DEST_CHANNEL_ID)
            if dest_channel:
                await dest_channel.send(decrypted_message)
                print(f"Sent decrypted message to destination channel.")
        except Exception as e:
            print(f"Failed to decrypt message: {e}")

    await bot.process_commands(message)

# Run the bot
bot.run(TOKEN)
