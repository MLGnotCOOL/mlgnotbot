import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import math
import random

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

app_id = "1397840600497131660"
public_key = "62337db9c45d967aad2ea3b2594bfba7f18e1b43687c505034db8533585a247f"

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"MLGnotBot is ready to go!")


@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the Server! {member.name}")


@bot.slash_command(name="hello", description="Hello World!")
async def hello(ctx):
    await ctx.respond(f"{ctx.author.mention}, Hello World!")


@bot.slash_command(name="roll_a_dice", description="roll a dice!")
async def roll_a_dice(ctx, face):
    if face.isnumeric():
        num = str(random.randint(1, int(face)))
        await ctx.respond(f"You Rolled a {num}!")
    else:
        await ctx.respond(f"bro u need to input a number...")


@bot.slash_command(name="gay_test", description="definitely a normal test!")
async def gay_test(ctx, testusr):
    await ctx.respond(f"user: {testusr}")


bot.run(TOKEN)