import requests
import json

def aio(text):
    url = "https://xu.su/api/send"
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
