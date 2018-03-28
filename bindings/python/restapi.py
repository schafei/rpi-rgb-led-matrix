#!/usr/bin/env python
from flask  import Flask, jsonify, request, render_template
from textdisplayer2 import textdisplayer

display = { 'text': 'Hello Vikings :-)', 'textcolor': ['255', '0', '0'], 'bgcolor': ['0', '0', '0'], 'scroll': false, 'blink': false }
textDisplayer = textdisplayer()
mainRoute = '/display'
app = Flask(__name__, static_url_path = mainRoute)

def request_wants_json():
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']

@app.route(mainRoute + '/', methods=['GET','POST','PUT','DELETE'])
def routing():

    if request_wants_json(): json = True
    else:                    json = False

    if request.method == 'GET':
        result = { display['text'], display['textcolor'], display['bgcolor'], display['scroll'], display['blink'] } 
        if json: return jsonify(result)
        else:    return '{ ' + display['text'] + ', ' + display['textcolor'] + ' , ' + display['bgcolor'] + ' , ' + display['scroll'] + ' , ' + display['blink'] + ' }' 

    elif request.method == 'PUT':
        display['text'] = request.form.get('text')
        display['textcolor'] = request.form.get('textcolor')
        display['bgcolor'] = request.form.get('bgcolor')
        display['scroll'] = request.form.get('scroll')
        display['blink'] = request.form.get('blink')
        textDisplayer.displayText(display['text'], display['textcolor'], display['bgcolor'], display['scroll'], display['blink'])

        result = { display['text'], display['textcolor'], display['bgcolor'], display['scroll'], display['blink'] } 
        if json: return jsonify(result), 201
        else:    return '{ ' + display['text'] + ', ' + display['textcolor'] + ' , ' + display['bgcolor'] + ' , ' + display['scroll'] + ' , ' + display['blink'] + ' }', 201

if __name__ == '__main__':
    app.run(debug = True, host = '127.0.0.1', threaded = False, use_reloader = False)
