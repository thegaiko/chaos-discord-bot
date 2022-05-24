import eel
from mongo import checkTOKEN
from inter import main

eel.init("/Users/gev.sb/Chaos/AI/web")

@eel.expose
def recv_data(access_token, ds_token, channel, delay):
    if checkTOKEN(access_token)==True:
        main(ds_token, channel, delay)
    else:
        print("error")
        exit()


eel.start("index.html", size=(700, 700))