from email import message
from os import access
from tracemalloc import start
import discord
import secrets
import datetime
import json
import asyncio
from config import BOT_TOKEN, PRICE, MEMBER_ROLE, TRAIL_MEMBER_ROLE, PUBLIC_MEMBER_ROLE
from mongo import createUser, checkSub, takeName, subscribe, checkUser, getRequestsList, delReq, verifyDb, addAvatar
from discord.ext import commands
from discord.ext.commands import Bot
from get_price import price_list
from asyncio import sleep

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

acceses = []
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
async def requestsList(ctx):
    requests = getRequestsList()
    for request in requests:
        emb = discord.Embed(title=f"Модерация заявок", color=ctx.message.author.color)
        emb.add_field(name="ID", value=request['id'], inline=False)
        emb.add_field(name="Имя", value=request['name'], inline=False)
        emb.add_field(name="Discord", value=request['discord'], inline=False)
        emb.add_field(name="Email", value=request['email'], inline=False)
        emb.add_field(name="О себе", value=request['about'], inline=False)
        await ctx.send(embed = emb)


@bot.command()
async def acceptRequest(ctx, id):
    delReq(id)
    token = secrets.token_hex(16)
    model = {"name": "-", "id": '-', "token": token, "avatar": "-", "price": "-", "start_date": "-", "end_date": "-", "retry": "-"}
    createUser(model)
    emb = discord.Embed(title=f"Токен", color=ctx.message.author.color)
    emb.add_field(name="Новый токен для пользователья.", value=f"```{token}```", inline=False)
    await ctx.send(embed = emb)

@bot.command()
async def addAva(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    avatar = member.avatar_url
    name = member.display_name
    id = member.id
    start_date = datetime.datetime.now()
    delta = datetime.timedelta(days=int(7))
    end_date = start_date + delta
    addAvatar(name, id, start_date, end_date, str(avatar))

@bot.command()
async def verify(ctx, token):
    await ctx.message.delete()
    member = ctx.message.author
    name = member.display_name
    id = member.id
    start_date = datetime.datetime.now()
    delta = datetime.timedelta(days=int(7))
    end_date = start_date + delta
    avatar = member.avatar_url
    verifyDb(name, id, start_date, end_date, str(avatar), token)
    role = member.guild.get_role(role_id=MEMBER_ROLE)
    await member.add_roles(role)
    emb = discord.Embed(title=f"Добро пожаловать {name}!", color=ctx.message.author.color)
    await ctx.author.send(embed = emb)

@bot.command()
async def generateToken(ctx):
    await ctx.message.delete()
    token = secrets.token_hex(16)
    model = {"name": "-", "id": '-', "token": token, "avatar": "-", "price": "-", "start_date": "-", "end_date": "-", "retry": "-"}
    createUser(model)
    emb = discord.Embed(title=f"Токен", color=ctx.message.author.color)
    emb.add_field(name="Новый токен для пользователья.", value=f"```{token}```", inline=False)
    await ctx.send(embed = emb)
    

@bot.command()
async def clear(message):
    async for msg in message.channel.history():
        await msg.delete()

@bot.event
async def on_member_join(member:discord.Member = None):
    role = member.guild.get_role(role_id=PUBLIC_MEMBER_ROLE)
    await member.add_roles(role)
    #создание ячейки в бд
    #name = member.display_name
    #id = member.id
    #token = secrets.token_hex(16)
    #start_date = datetime.datetime.now()
    #avatar = member.avatar_url
    #delta = datetime.timedelta(days=int(7))
    #end_date = start_date + delta
    #model = {"name": name, "id": id, "token": token, "avatar": avatar, "price": PRICE, "start_date": start_date, "end_date": end_date, "retry": 0}
    #createUser(model)


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
async def getToken(ctx):
    await ctx.message.delete()
    model = checkUser(int(ctx.author.id))
    emb = discord.Embed(title=f"Персональный токен для пользователя {model[0]}", color=ctx.message.author.color)
    emb.add_field(name="TOKEN", value=f"```{model[2]}```", inline=False)
    emb.add_field(name="Дата окончания подписки", value=model[5], inline=False)
    await ctx.author.send(embed = emb)


@bot.command()
async def check(ctx, *, message):
    if ctx.author.id in acceses:
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
    else: 
        embed1 = discord.Embed(
            description=f'Извините, у вас нет доступа.', color=0x08b00ff)
        await ctx.send(embed=embed1)

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
