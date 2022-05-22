import requests
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
from threading import *

url = "https://api.vk.com/method/wall.get"
names = ["uinft", "bitcoin_to_the_moon", "moneyunknown", "scroogeboy", "money_scrooge", "cryptomskclub", "sevaexp"]  # тут никнеймы сообществ
offsets = [1, 1, 1, 1, 1, 1, 1]  # при наличии закрепа поставить 1 при отцувствии 0
counts =  [2, 2, 2, 2, 2, 2, 2]  # при наличии закрепа поставить 2 при отцувствии 1


webhook = DiscordWebhook(
    url='https://discord.com/api/webhooks/977908469497737257/DpUpND_e60mYoNXmAjCabeAw6gUpwC3C3pLyeJhE4HL7XJny2gjBe3KSTvJpEXQ79S-z')


def post_check(name, offset, count):
    payload = f'domain={name}&offset={offset}&count={count}&extended=false&access_token=0b97751f0b97751f0b97751f920bec1a5500b970b97751f698deca772c621f6c27724c3&v=5.131'
    headers = {
        'authority': 'api.vk.com',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'origin': 'https://dev.vk.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://dev.vk.com/',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    id0 = response.json()['response']['items'][0]['id']
    while True:
        response = requests.request("POST", url, headers=headers, data=payload)
        id = response.json()['response']['items'][0]['id']
        text = response.json()['response']['items'][0]['text']
        if id0 < id:
            try:
                response.json()[
                    'response']['items'][0]['attachments'][0]['photo']['sizes'][0]['url']
            except KeyError:
                embed = DiscordEmbed(
                    title=name, description=text, url=f'https://vk.com/{name}', color='5a359c')
                embed.set_footer(
                    text='VK', icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/VK.com-logo.svg/2048px-VK.com-logo.svg.png')
                webhook.add_embed(embed)
                print(text)
                response = webhook.execute()
            else:
                webhook.remove_embeds()
                photo = response.json()[
                    'response']['items'][0]['attachments'][0]['photo']['sizes'][len(response.json()[
                        'response']['items'][0]['attachments'][0]['photo']['sizes'])-1]['url']
                embed = DiscordEmbed(title=name, url=f'https://vk.com/{name}', image={
                    "url": photo}, description=text, color='5a359c')
                embed.set_footer(
                    text='VK', icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/VK.com-logo.svg/2048px-VK.com-logo.svg.png')
                webhook.add_embed(embed)
                response = webhook.execute()

        id0 = id
        print(id0)
        time.sleep(1)


t = []

for i in range(len(names)):
    t.append(Thread(target=post_check, args=(
        names[i], offsets[i], counts[i],)))
    t[i].start()