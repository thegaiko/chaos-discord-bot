import snscrape.modules.twitter as twitterScraper
from discord_webhook import DiscordWebhook, DiscordEmbed
from threading import Thread
import time


webhook_url = 'https://discord.com/api/webhooks/977908867948216380/mI3IJG8MSLcBj0vswTFhC7hcMS-hoyytOuaxVceHMGEymAuZTa8qD8mv0dh9LwHSX6qq'

targets = ['AneroVerse', 'cubexnft', 'opensea_support', "elonmusk"]
tweets = []
model = []

def get(target):
    scraper = twitterScraper.TwitterUserScraper(target, False)
    for i, tweet in enumerate(scraper.get_items()):
        if i > 1:
            break
        tweets.append(tweet.content)
        if not tweet.media:
            continue
        model.append(tweet.user.username)
        model.append(tweet.user.displayname)
        model.append(tweet.content)
        model.append(tweet.media[0].previewUrl)
        
        


def main(target):
    get(target)
    last = tweets[0]

    while True:
        get(target)
        print(tweets)
        if last == tweets[1]:
            last = tweets[0]
            webhook = DiscordWebhook(url=webhook_url)
            embed = DiscordEmbed(title=f"{model[0]} ({model[1]})", description=model[2], image={"url": model[3]}, color=0x3000ff)
            webhook.add_embed(embed)
            webhook.execute()
            model.clear()
        tweets.clear()
        time.sleep(60)

t=[]
for i in range(len(targets)):
    t.append(Thread(target=main, args=(targets[i],)))
    t[i].start()