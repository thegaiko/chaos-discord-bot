from curses.ascii import DEL, US
from flask import Flask, request, jsonify
from mongo import checkTOKEN
from inter import main
import json
app = Flask(__name__)

@app.route('/ai', methods=['POST'])
def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        AUTH_TOKEN = json["AUTH_TOKEN"]
        DS_TOKEN = json["DS_TOKEN"]
        CHANNEL = json["CHANNEL"]
        USER = json["USER"]
        DELAY = json["DELAY"]
        if checkTOKEN(AUTH_TOKEN)==True:
            main(DS_TOKEN, CHANNEL, USER, DELAY)
            return 'Process started'
        else:
            return 'auth failed'
    else:
        return 'Content-Type not supported!'

if __name__ == "__main__":
    app.run(debug=True)
