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

gay_list = [
    "summeryou7101",
];

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
    if face.isdecimal():
        if int(face) < 1:
            await ctx.respond(f"bro i need a number bigger than 1")
        else:
            num = str(random.randint(1, int(face)))
            await ctx.respond(f"You Rolled a {num}!")
    else:
        await ctx.respond(f"bro u need to input a number...")


@bot.slash_command(name="gay_test", description="definitely a normal test!")
async def gay_test(ctx, member: discord.Member):
    gay_meter = 0
    if (member.name in gay_list):
        gay_meter = random.randint(50, 100)
    else:
        gay_meter = random.randint(0, 100)
    
    embed = discord.Embed(
        title = f"Is {member.nick or member.global_name or member.name} gay?",
        description=f"{member.nick or member.global_name or member.name} is {gay_meter}% gay!",
    )
    embed.set_thumbnail(url=member.display_avatar)

    await ctx.respond(embed=embed)


bot.run(TOKEN)