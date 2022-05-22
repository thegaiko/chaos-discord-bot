import requests

coins = ["BTCUSDT", "BNBUSDT", "ETHUSDT", "SOLUSDT",
         "WAXPUSDT", "NEARUSDT", "AVAXUSDT", "DOTUSDT"]

coin_name = ["BTC", "BNB", "ETH", "SOL", "WAXP", "NEAR", "AVAX", "DOT"]


def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    payload = {}
    headers = {
        'X-MBX-APIKEY': 'Ck480XhG1yxuouleqYhoRahuL8l7SlPWWRgd70IprJLbFa3n80ObjWX6zFsA0Oz1'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    res = str(response.json()["price"])
    l = len(res)
    res = res[:l-6]

    return(res)


def price_list():
    prices = []
    for i in range(len(coins)):
        prices.append(f"{coin_name[i]} - {get_price(coins[i])}$")
    return(prices)