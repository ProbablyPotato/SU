import logging
import os
import discord
import asyncio
import random
from collections import defaultdict

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
client = discord.Client(intents=intents)

# Set up logging for the bot
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("DISCORD_TOKEN")
IMAGE_FOLDER = './images'  # Local folder with images
CHANNEL_ID = 123456789012345678  # Replace with your channel ID
BANG_WORD = 'bang!'

# If token is missing, exit
if not TOKEN:
    logging.error(f"Missing required token")
    exit(1)

# Background worker function
async def background_worker():
    while True:
        logging.info("Background worker is running")
        await asyncio.sleep(30)


# Event when the bot is ready
@client.event
async def on_ready():
    try:
        logging.info(f"We have logged in as {client.user}")
        client.loop.create_task(background_worker())
        logging.info("Started background worker task")
    except Exception as e:
        logging.error(f"Error while trying to start background worker: {e}")


# Event when a message is received by the bot
@client.event
async def on_message(message):
    try:
        if message.author == client.user:
            return
    
        if message.content.lower() == 'hello':
            await message.channel.send(f"Hello {message.author.global_name}!")
            return
    
        elif message.content.lower() == 'bye':
            await message.channel.send(f"Goodbye {message.author.global_name}!")
            return
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        await message.channel.send(f"An error occurred while trying to process your request. Please try again later.")


# Start the bot with a token
if __name__ == '__main__':
    try:
        client.run(TOKEN)
    except Exception as e:
        logging.error(f"Error while trying to start the bot: {e}")



# Start running chicken hunt
bot = commands.Bot(command_prefix='/', intents=intents)

# In-memory score tracking
scores = defaultdict(int)

# Control flag
image_active = False
image_message_id = None
winner = None

# Background task to send random image at random ~30 min intervals
@tasks.loop(seconds=10)  # Checks every 10s if it's time
async def post_random_image():
    if not image_active:
        wait_time = random.randint(1100, 2300)  # ~a range of minutes
        await asyncio.sleep(wait_time)

        image_file = random.choice(os.listdir(IMAGE_FOLDER))
        image_path = os.path.join(IMAGE_FOLDER, image_file)

        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            global image_active, image_message_id, winner
            image_active = True
            winner = None
            msg = await channel.send(file=discord.File(image_path))
            image_message_id = msg.id
            print(f"Posted image {image_file}, waiting for 'Bang!'")


@bot.event
async def on_message(message):
    global image_active, winner

    await bot.process_commands(message)  # Allow commands to run

    if (
        image_active and
        message.channel.id == CHANNEL_ID and
        message.content.lower().strip() == BANG_WORD and
        not message.author.bot
    ):
        if winner is None:
            winner = message.author
            scores[winner.id] += 1
            await message.channel.send(f"🎯 {winner.mention} got it first! You now have {scores[winner.id]} point(s).")
            image_active = False
        else:
            await message.channel.send(f"⏱ Too late, {message.author.mention}! {winner.mention} was quicker!")


@bot.command(name='hunt')
    if hunt_running == 0 :   
        hunt_running = 1
        let CHANNEL_ID = message.channel.id
        post_random_image.start()  # Start the task loop
        ctx.send("Hunt started.")
else:
        ctx.send("Hunt is already running.")


@bot.command(name='score')
async def show_scores(ctx):
    if not scores:
        await ctx.send("🏆 No scores yet.")
        return

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    message = "**📊 Scoreboard:**\n"
    for uid, points in sorted_scores:
        user = await bot.fetch_user(uid)
        message += f"• {user.name}: {points} point(s)\n"
    await ctx.send(message)


@bot.command(name='clearscores')
@commands.has_permissions(administrator=True)
async def clear_scores(ctx):
    scores.clear()
    await ctx.send("🧹 Scores cleared!")


# Error handling
@clear_scores.error
async def clear_scores_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to do that.")
