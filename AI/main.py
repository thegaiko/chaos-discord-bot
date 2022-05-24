from fastapi import FastAPI
from typing import Optional
from playwright.sync_api import sync_playwright
import random
import time

from PIL import Image, ImageTk
import tkinter as tk
from threading import Thread
import time

def photo_show():
    master = tk.Tk()  
    canvas = tk.Canvas(master, height=1000  , width=1000)
    image = Image.open("/Users/gev.sb/Chaos/screenshot.png")
    photo = ImageTk.PhotoImage(image)
    image = canvas.create_image(0, 0, anchor='nw',image=photo)
    canvas.grid(row=2,column=1)

    master.mainloop()

    tk.mainloop()

messages = [
    'Ive been tryna call',
    'Ive been on my own for long enough',
    'Maybe you can show me how to love, maybe',
    'Im going through withdrawals',
    'You dont even have to do too much',
    'You can turn me on with just a touch, baby',
    'I look around and',
    'Sin Citys cold and empty',
    'No ones around to judge me',
    'I cant see clearly when youre gone',
    'I said, ooh, Im blinded by the lights',
    'No, I cant sleep until I feel your touch',
    'I said, ooh, Im drowning in the night',
    'Oh, when Im like this, youre the one I trust',
    'Im running out of time',
    'Cause I can see the sun light up the sky',
    'So I hit the road in overdrive, baby, oh',
    'The citys cold and empty(oh)',
    'No ones around to judge me(oh)',
    'I cant see clearly when youre gone',
]
def start_spam(link, count):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://discord.com/login")
        time.sleep(2)
        page.screenshot(path="screenshot.png", full_page=True)
        photo_show()
        print('Ожидание сканирования QR кода')
        time.sleep(15)
        page.screenshot(path='screen.png')
        page.goto(link)
        time.sleep(3)
        page.screenshot(path='screen.png')
        for i in range(int(count)):
            page.type('div[role="textbox"]',
                      messages[random.randint(0, len(messages))])
            page.keyboard.press('Enter')
        time.sleep(2)
        browser.close()