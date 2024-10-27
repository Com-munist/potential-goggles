import discord
import rsa
import os
import base64
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Define intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Required for reading message content

# Discord bot setup
Private_key = os.getenv('''-----BEGIN RSA PRIVATE KEY-----MIICUAIBAAJ+AIu36jbCC656iqAjZpR5bb5vla450v3aMcBfRWJXtl1jp5RrPcAatWxfWEAFCU1XVPTjj2ePNWpUuU0VKM9WE/GtQxsXjK6qUK8STLjZUDI7iFaj9lSCsDXwHdAuaPVs9H6m3SuT7caEKLdZJEoDx+nzJlHaNmHCkxPWUDIlAgMBAAECfR8MAESou/XKjzFkjG/jx8owe39apBL6wGFyCjX/Lav08BEf/3nHtZbeXPrk45tHE77TLlOh1AnLx91iogkvf/hE0vVZlQqz6UAu9rfjDaBAWC4K3l/25hnoX/pnqakXsoqXD4gM8tCs51b70YOkIo+n+p5E+Q5ijzk7WjmhAkMGqsXsEzW12pXVKug1MdGwYbBzK2UOXzf89FG9NkCBrcV3twcNFEARBzaZZt2qMeeQtVlZC6GW67JfrPLgcPFQE7wJ
AjsU9NpBWghPPJCcMB13O/RS5Uy9wJIdia/SU8Kro50NoqYJApAXoi+y2HBbHNp8mE75j0GrknSeRNpEPQJDBabJc96szuTl0fc3M7BxcbS9oEMOvOoWScTJbT0J3WNyWpK51WpvDIAy1kKOcHExPEed34+ugIJ3iAbRM1RKGnlAEQI7CFHUvBEkL2DaAEfRyt5QdwB1YPesinF5DcUXCdEgrqMdy4Hq9pb63MO0h1eDHefRop3O8nBoP9UR2fkCQwTbLIjWTl1u5UQ/1RJUYUXTfnmmvRNyixYuc91VaPyrQ09pqNqTQpvSktWZ4XJwUEiwXaqrWAwOuUl6l6E/XFP4nyQ=-----END RSA PRIVATE KEY-----''')
TOKEN = os.getenv('DISCORD_TOKEN_APPLE')
SOURCE_CHANNEL_ID = int(os.getenv('SOURCE_CHANNEL_ID'))
DEST_CHANNEL_ID = int(os.getenv('DEST_CHANNEL_ID'))

# Convert PEM format private key to RSA key object
try:
    privateKey = rsa.PrivateKey.load_pkcs1(Private_key)
    print("Private key loaded successfully.")
except Exception as e:
    print(f"Error loading private key: {e}")

# Initialize the bot
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print(f"Source Channel ID: {SOURCE_CHANNEL_ID}")
    print("Bot is ready to read messages!")

@bot.event
async def on_message(message):
    print("on_message triggered")  # Check if this prints at all
    print(f"Received message: {message.content} from {message.author.name} in channel {message.channel.id}")

    # Check if message is from the source channel
    if message.channel.id == SOURCE_CHANNEL_ID:
        print(f"Raw received message content: {message.content}")

        encrypted_message = message.content.strip()  # Remove any extra spaces
        try:
            # Step 1: Decode base64 message
            try:
                encrypted_bytes = base64.b64decode(encrypted_message)
                print("Base64 decoding successful.")
            except Exception as decode_error:
                print(f"Failed to decode base64: {decode_error}")
                return  # Exit if base64 decoding fails
            
            # Step 2: RSA decryption
            try:
                decrypted_message = rsa.decrypt(encrypted_bytes, privateKey).decode('utf-8')
                print(f"Decrypted message: {decrypted_message}")
            except Exception as decrypt_error:
                print(f"Failed to decrypt message: {decrypt_error}")
                return  # Exit if decryption fails
            
            # Step 3: Send decrypted message to destination channel
            dest_channel = bot.get_channel(DEST_CHANNEL_ID)
            if dest_channel:
                await dest_channel.send(decrypted_message)
                print("Sent decrypted message to destination channel.")
            else:
                print("Destination channel not found.")
                
        except Exception as e:
            print(f"Unexpected error: {e}")

    await bot.process_commands(message)
@bot.command()
async def test(ctx):
    await ctx.send("Bot is receiving commands!")
    
# Run the bot
bot.run(TOKEN)

