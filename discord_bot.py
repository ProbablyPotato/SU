import logging
import os
import discord
import asyncio
import random
# from close_server import *
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

# set parameters to close the server overnight: CLOSED_ROLE_ID is applied to everyone who is routinely in the STANDARD_ROLE_ID role, and then removed again in the morning. 
# times are definable below.

# IDs of the roles you want to manage
CLOSED_ROLE_NAME = 'server-closed'
STANDARD_ROLE_NAME = 'members'


# Set the times when server should shut down and reopen
APPLY_TIME = '12:58'  # 10 PM
REMOVE_TIME = '17:33'  # 7 AM

#create scheduler
scheduler = AsyncIOScheduler()

# run the function to begin opening/closing the server daily
@client.event
async def on_ready():
    print(f"Is now running!")
    await start_schedule()



# Function to apply the role to all members with the specified role
async def apply_role():
    guild = client.get_guild(guild_id)
    
    apply_role = discord.utils.get(guild.roles, name=CLOSED_ROLE_NAME)
    usual_role = discord.utils.get(guild.roles, name=STANDARD_ROLE_NAME)
    
    for member in guild.members:
        if usual_role in member.roles and apply_role not in member.roles:
            await member.add_role(apply_role)

    print(f"Applied role {apply_role.name} to all members with role {usual_role.name}")

# Function to remove the role from all members
async def remove_role():
    guild = client.get_guild(guild_id)
    apply_role = discord.utils.get(guild.roles, name=CLOSED_ROLE_NAME)
    usual_role = discord.utils.get(guild.roles, name=STANDARD_ROLE_NAME)

    for member in guild.members:
        if usual_role in member.roles and apply_role in member.roles:
            await member.remove_role(apply_role)

    print(f"Removed role {apply_role.name} from all members")


# Function to start the server lockdown between given hours
async def start_schedule():
    print(f'Bot scheduler has been triggered!')
   
    # Set up the scheduler to run the functions at the specified times
    scheduler.add_job(apply_role, 'cron', hour=APPLY_TIME.split(':')[0], minute=APPLY_TIME.split(':')[1])
    scheduler.add_job(remove_role, 'cron', hour=REMOVE_TIME.split(':')[0], minute=REMOVE_TIME.split(':')[1])
    scheduler.start()





















client.run(TOKEN)




