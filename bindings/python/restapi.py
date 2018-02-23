#!/usr/bin/env python
from flask  import Flask, jsonify, request, render_template
#from textdisplayer import textdisplayer

display = { 'text': 'Hello Vikings :-)', 'status': 'on' }
#textDisplayer = textdisplayer()
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
        result = { display['text'], display['status'] } 
        if json: return jsonify(result)
        else:    return '{ ' + display['text'] + ', ' + display['status'] + ' }' 

    elif request.method == 'PUT':
        text = request.form.get('text')
        status = request.form.get('status')
        if text:
            display['text'] = text
            #textDisplayer.displayText(text, 1)
        if status:
            display['status'] = status

        result = { display['text'], display['status'] }
        return jsonify({"status": False}), 201

if __name__ == '__main__':
    app.run(debug = False, host = '0.0.0.0', threaded = False, use_reloader = True)
