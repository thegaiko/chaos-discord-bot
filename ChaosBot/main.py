import discord
import secrets
import datetime
import json
import asyncio
from config import BOT_TOKEN, PRICE, MEMBER_ROLE, TRAIL_MEMBER_ROLE, PUBLIC_MEMBER_ROLE
from mongo import createUser, checkSub, takeName, subscribe, checkUser
from discord.ext import commands
from discord.ext.commands import Bot
from get_price import price_list
from asyncio import sleep

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    while True:
        price = price_list()
        stop = 20
        time = 0
        while time < stop:
            for text in price:
                await bot.change_presence(status=discord.Status.online, activity=discord.Game(text))
                await sleep(3)
            time += 1

@bot.command()
async def clear(message):
    async for msg in message.channel.history():
        await msg.delete()

@bot.event
async def on_member_join(member:discord.Member = None):
    role = member.guild.get_role(role_id=PUBLIC_MEMBER_ROLE)
    await member.add_roles(role)
    #создание ячейки в бд
    name = member.display_name
    id = member.id
    token = secrets.token_hex(16)
    start_date = datetime.datetime.now()
    delta = datetime.timedelta(days=int(7))
    end_date = start_date + delta
    model = {"name": name, "id": id, "token": token, "price": PRICE, "start_date": start_date, "end_date": end_date, "retry": 0}
    createUser(model)


@bot.command()
async def addDB(ctx,member:discord.Member = None, guild: discord.Guild = None):
    await ctx.message.delete()
    name = member.display_name
    id = member.id
    token = secrets.token_hex(16)
    start_date = datetime.datetime.now()
    delta = datetime.timedelta(days=int(7))
    end_date = start_date + delta
    model = {"name": name, "id": id, "token": token, "price": PRICE, "start_date": start_date, "end_date": end_date, "retry": 0}
    createUser(model)

@bot.command()
async def check(ctx, *, message):
    await ctx.message.delete()
    model = checkUser(int(message))
    emb = discord.Embed(title="Информация о пользователе.", color=ctx.message.author.color)
    emb.add_field(name="Никнейм", value=model[0], inline=False)
    emb.add_field(name="ID", value=model[1], inline=False)
    emb.add_field(name="Token", value=model[2], inline=False)
    emb.add_field(name="Цена подписки", value=model[3], inline=False)
    emb.add_field(name="Дата начала", value=model[4], inline=False)
    emb.add_field(name="Дата конца", value=model[5], inline=False)
    emb.add_field(name="Попытки", value=model[6], inline=False)

    await ctx.send(embed = emb)

@bot.command()
async def subCheck(ctx):
    await ctx.message.delete()
    kickMembers = checkSub()
    emb = discord.Embed(title="Список пользователей у которых проспрочилась подписка.", color=ctx.message.author.color)
    for member in kickMembers:
        nick = takeName(member)

        role = member.guild.get_role(role_id=MEMBER_ROLE)
        await member.remove_roles(role)
        role = member.guild.get_role(role_id=PUBLIC_MEMBER_ROLE)
        await member.add_roles(role)

        emb.add_field(name=nick, value=member, inline=False)
        
    await ctx.send(embed = emb)

@bot.command()
async def sub(ctx, member: discord.Member):
    await ctx.message.delete()
    subscribe(member.id)
    role = member.guild.get_role(role_id=PUBLIC_MEMBER_ROLE)
    await member.remove_roles(role)
    role = member.guild.get_role(role_id=MEMBER_ROLE)
    await member.add_roles(role)
    emb = discord.Embed(description=f"Вы одобрили членство **{member.display_name}**", color=ctx.message.author.color)
    await ctx.send(embed = emb)


bot.run(BOT_TOKEN)