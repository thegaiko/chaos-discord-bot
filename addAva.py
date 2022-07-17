import discord 
from mongo import addAva
from config import BOT_TOKEN

from discord.ext import commands
from discord.ext.commands import Bot
from get_price import price_list
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.command()
async def avatar(ctx, *, avamember : discord.Member=None):
    user = '850453564488941569'
    userAvatarUrl = discord.Member(user).avatar_url
    #addAva({'id': avamember})
    await ctx.send(userAvatarUrl)

bot.run(BOT_TOKEN)


