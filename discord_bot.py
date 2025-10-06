import logging
import os
import discord
import asyncio
import random
import close_server
from collections import defaultdict
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
client = discord.Client(intents=intents)

# Set up logging for the bot
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("DISCORD_TOKEN")

# set parameters to close the server overnight: CLOSED_ROLE_ID is applied to everyone who is routinely in the STANDARD_ROLE_ID role, and then removed again in the morning. 
# times are definable below.

# IDs of the roles you want to manage
CLOSED_ROLE_ID = 'server-closed'
STANDARD_ROLE_ID = 'members'

# Set the times when server should shut down and reopen
APPLY_TIME = '18:22'  # 10 PM
REMOVE_TIME = '17:30'  # 7 AM

client.run(TOKEN)

# run the function to begin opening/closing the server daily
on_ready(ctx):
    await ctx.send("successful")

