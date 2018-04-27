#!/usr/bin/env python
from flask  import Flask, jsonify, request, render_template
from textdisplayer2 import textdisplayer

display = { 'imagepath': '', 'text': 'Hello Vikings :-)', 'textcolor': ['255', '0', '0'], 'bgcolor': ['0', '0', '0'], 'scroll': 'false', 'blink': 'false' }
textDisplayer = textdisplayer()
mainRoute = '/display'
app = Flask(__name__, static_url_path = mainRoute)

@app.route(mainRoute + '/', methods=['GET','POST','PUT','DELETE'])
def routing():

    if request.method == 'GET':
        jsonify(display)

    elif request.method == 'PUT':
        display['imagepath'] = ''
        display['text'] = request.json.get('text')
        display['textcolor'] = request.json.get('textcolor')
        display['bgcolor'] = request.json.get('bgcolor')
        display['scroll'] = request.json.get('scroll')
        display['blink'] = request.json.get('blink')
        print("text: " + display['text'])
        textDisplayer.displayText(display['imagepath'], display['text'], display['textcolor'], display['bgcolor'], display['scroll'], display['blink'])
        return jsonify(display), 201

if __name__ == '__main__':
    app.run(debug = True, host = '127.0.0.1', threaded = False, use_reloader = False)
