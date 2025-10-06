import logging
import os
import discord
import asyncio
import random
from collections import defaultdict
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
client = discord.Client(intents=intents)

# Set up logging for the bot
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("DISCORD_TOKEN")

# Replace these with your own bot token and the IDs of the roles you want to manage
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
CLOSED_ROLE_ID = 'server-closed'
STANDARD_ROLE_ID = 'members'

# Set the times when the role should be applied and removed
APPLY_TIME = '22:00'  # 10 PM
REMOVE_TIME = '07:00'  # 7 AM

