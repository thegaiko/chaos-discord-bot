from telethon import TelegramClient, events, functions
from discord_webhook import DiscordWebhook, DiscordEmbed
from threading import *
import requests
import json

names = ("AlienCripto", "waxdrop", "swoptoky", "arbuzery_money", "tradeparty1337", "AlienCripto", "undercryptog", "CryptoAndBounty", "dekigang", "drivecrypto", "jimbo_nft", "whitelist1")
webhook_url = 'https://discord.com/api/webhooks/977873211255558174/VPKcJXD9Ub6FplGERRHnL9kwhr5HAOyzU4oRmMnhApJ0wk-9T1vBs9FGqV1FugKuRFlS'

api_id = '18090282'
api_hash = '6e8d8ec18773de0bfe183b1da0975c89'
client = TelegramClient('session_name', api_id, api_hash)
client.start()



def monitorChannel(channel_name): 
    @client.on(events.NewMessage(chats=(channel_name)))
    async def normal_handler(event):
        webhook = DiscordWebhook(url=webhook_url)
        message_text = event.message.message
        print(message_text)
        message_url = "https://t.me/" + channel_name + "/" + str(event.message.id)
        if len(message_text) > 0:
            embed = DiscordEmbed(title=channel_name, description=message_text, url=message_url, color=0x3000ff)
            embed.set_footer(text='Telegram', icon_url='https://pnggrid.com/wp-content/uploads/2021/04/telegram-logo-circle-1024x1024.png')
            webhook.add_embed(embed)
            webhook.execute()

for name in names:
    monitorChannel(name)

client.run_until_disconnected()