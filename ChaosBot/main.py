import discord
import secrets
import datetime
import json
import asyncio
from config import BOT_TOKEN, PRICE, MEMBER_ROLE, TRAIL_MEMBER_ROLE, PUBLIC_MEMBER_ROLE
from mongo import createUser, checkSub, takeName,subscribe
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
async def info(ctx,member:discord.Member = None, guild: discord.Guild = None):
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
    subscribe(member.id)
    role = member.guild.get_role(role_id=TRAIL_MEMBER_ROLE)
    await member.remove_roles(role)
    role = member.guild.get_role(role_id=MEMBER_ROLE)
    await member.add_roles(role)


#выдача роли
@bot.command(name="selfrole")
async def self_role(ctx):
    await ctx.send("Answer These Question In Next 2Min!")

    questions = ["Enter Message: ", "Enter Emojis: ", "Enter Roles: ", "Enter Channel: "]
    answers = []

    def check(user):
        return user.author == ctx.author and user.channel == ctx.channel
    
    for question in questions:
        await ctx.send(question)

        try:
            msg = await bot.wait_for('message', timeout=120.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Type Faster Next Time!")
            return
        else:
            answers.append(msg.content)

    emojis = answers[1].split(" ")
    roles = answers[2].split(" ")
    c_id = int(answers[3][2:-1])
    channel = bot.get_channel(c_id)

    bot_msg = await channel.send(answers[0])

    with open("selfrole.json", "r") as f:
        self_roles = json.load(f)

    self_roles[str(bot_msg.id)] = {}
    self_roles[str(bot_msg.id)]["emojis"] = emojis
    self_roles[str(bot_msg.id)]["roles"] = roles

    with open("selfrole.json", "w") as f:
        json.dump(self_roles, f)

    for emoji in emojis:
        await bot_msg.add_reaction(emoji)

@bot.event
async def on_raw_reaction_add(payload):
    msg_id = payload.message_id

    with open("selfrole.json", "r") as f:
        self_roles = json.load(f)

    if payload.member.bot:
        return
    
    if str(msg_id) in self_roles:
        emojis = []
        roles = []

        for emoji in self_roles[str(msg_id)]['emojis']:
            emojis.append(emoji)

        for role in self_roles[str(msg_id)]['roles']:
            roles.append(role)
        
        guild = bot.get_guild(payload.guild_id)

        for i in range(len(emojis)):
            choosed_emoji = str(payload.emoji)
            if choosed_emoji == emojis[i]:
                selected_role = roles[i]

                role = discord.utils.get(guild.roles, name=selected_role)

                await payload.member.add_roles(role)
                await payload.member.send(f"You Got {selected_role} Role!")

@bot.event
async def on_raw_reaction_remove(payload):
    msg_id = payload.message_id

    with open("selfrole.json", "r") as f:
        self_roles = json.load(f)
    
    if str(msg_id) in self_roles:
        emojis = []
        roles = []

        for emoji in self_roles[str(msg_id)]['emojis']:
            emojis.append(
                emoji)

        for role in self_roles[str(msg_id)]['roles']:
            roles.append(role)
        
        guild = bot.get_guild(payload.guild_id)

        for i in range(len(emojis)):
            choosed_emoji = str(payload.emoji)
            if choosed_emoji == emojis[i]:
                selected_role = roles[i]

                role = discord.utils.get(guild.roles, name=selected_role)

                member = await(guild.fetch_member(payload.user_id))
                if member is not None:
                    await member.remove_roles(role)

bot.run(BOT_TOKEN)