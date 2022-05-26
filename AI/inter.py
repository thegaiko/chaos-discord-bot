import discum
import os
from base import message_base
from req import aio
from mongo import checkTOKEN
import random
import time
from threading import Thread
from datetime import datetime


def main(TOKEN, CHANNEL_ID, USER, DELAY):
    bot = discum.Client(token = TOKEN, log=False)
    
    last_mention = [datetime.now()]

    @bot.gateway.command
    def helloworld(resp):

        if resp.event.ready_supplemental: #ready_supplemental is sent after ready
            user = bot.gateway.session.user
            print("Logged in as {}#{}".format(user['username'], user['discriminator']))
        
        if resp.event.message:
                m = resp.parsed.auto()
                channelID = m['channel_id']
                username = m['author']['username']
                content = m['content']
                if username == USER and content == 'bye': 
                    print("EXIT")
                    return ("End")
                if channelID == CHANNEL_ID and username != USER:
                    if m['type'] == 'reply':
                        if m["referenced_message"]["author"]["username"] == USER:
                            last_mention.append(datetime.now())
                            bot.sendMessage(CHANNEL_ID, aio(content))

    def randomizer():
        i = random.randint(0, (len(message_base) - 1))
        bot.sendMessage(CHANNEL_ID, message_base[i])
        while True:
            last = last_mention[-1]
            last = time.mktime(last.timetuple())
            now = datetime.now()
            now = time.mktime(now.timetuple())
            moment = now - last
            if moment > int(DELAY):
                i = random.randint(0, (len(message_base) - 1))
                bot.sendMessage(CHANNEL_ID, message_base[i])
                last_mention.append(datetime.now())

    def starter():
        bot.gateway.run(auto_reconnect=True)

    start = Thread(target=starter)
    start.start()
    random_start = Thread(target=randomizer)
    random_start.start()