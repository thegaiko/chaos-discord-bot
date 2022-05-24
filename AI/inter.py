from ast import arg
import discum
import requests
import json
from base import message_base
import random
import time
from threading import Thread
from pprint import pprint 
from datetime import datetime

bot = discum.Client(token = "ODUwNDUzNTY0NDg4OTQxNTY5.Gpfppw.ScZ29xmjbZsMqHX3VVLwFgSXVPpEIRQYU0ylXY", log=False)

url = "https://xu.su/api/send"

def aio(text):
    payload = json.dumps({
    "uid": None,
    "bot": "pbot",
    "text": text
    })
    headers = {
    'authority': 'xu.su',
    'accept': 'application/json',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json',
    'cookie': '_ym_uid=1651530561810861817; _ym_d=1651530561; _ym_isad=1; _ga=GA1.2.600410846.1651530561; _gid=GA1.2.739028486.1651530561; _xbs_pp=1651530568497',
    'origin': 'https://xu.su',
    'referer': 'https://xu.su/',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return(response.json()["text"])

last_mention = [datetime.now()]

@bot.gateway.command
def helloworld(resp):
    if resp.event.ready_supplemental: #ready_supplemental is sent after ready
        user = bot.gateway.session.user
        print("Logged in as {}#{}".format(user['username'], user['discriminator']))
    
    if resp.event.message:
            m = resp.parsed.auto()
            guildID = m['guild_id'] if 'guild_id' in m else None #because DMs are technically channels too
            channelID = m['channel_id']
            username = m['author']['username']
            discriminator = m['author']['discriminator']
            content = m['content']
            if channelID == '958364681871978547' and username != 'gaiko':
                message = content.split()
                if m['type'] == 'reply':
                    if m["referenced_message"]["author"]["username"] == 'gaiko':
                        last_mention.append(datetime.now())
                        bot.sendMessage("958364681871978547", aio(content))

def randomizer():
    i = random.randint(0, (len(message_base) - 1))
    bot.sendMessage("958364681871978547", message_base[i])
    while True:
        last = last_mention[-1]
        last = time.mktime(last.timetuple())
        now = datetime.now()
        now = time.mktime(now.timetuple())
        moment = now - last
        print(moment)
        if moment > 30:
            i = random.randint(0, (len(message_base) - 1))
            bot.sendMessage("958364681871978547", message_base[i])
            last_mention.append(datetime.now())

def starter():
    bot.gateway.run(auto_reconnect=True)

start = Thread(target=starter)
start.start()
random_start = Thread(target=randomizer)
random_start.start()