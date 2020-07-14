import discord
import os
import sys
sys.path.append(".")
from YTDLSource import YTDLSource
from discord.ext import commands

bot = commands.Bot(command_prefix = '>')
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cog.{extension}')
@bot.command()
async def unload(ctx,extension):
    extension = extension[:3]
    bot.unload_extension(f'cog.{extension}')
def is_guild_owner():
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
    return commands.check(predicate)
@bot.command()
@commands.check_any(commands.is_owner(), is_guild_owner())
async def only_for_owners(ctx):
    await ctx.send('Hello owner!')

bot.run("NzIzMzAwNDk5ODM4ODYxNDAy.XuvoMw.qH29RGW-RVl6f1ZxToOrZ0O9fQI")