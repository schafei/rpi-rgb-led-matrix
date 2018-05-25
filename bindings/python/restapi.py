#!/usr/bin/env python
import sys
from flask import Flask, jsonify, request, render_template
from signal import *
from contentdisplayer import contentdisplayer

display = { 'imagepath': '', 'text': 'Hello Vikings :-)', 'textcolor': ['255', '255', '255'], 'bgcolor': ['0', '0', '0'], 'scroll': 'true', 'blink': 'false' }
contentdisplayer = contentdisplayer()
mainRoute = '/display'
app = Flask(__name__, static_url_path = mainRoute)

@app.route(mainRoute + '/', methods=['GET','POST','PUT','DELETE'])
def routing():

  if request.method == 'GET':
    jsonify(display)

  elif request.method == 'PUT':
    imagename = request.json.get('imagename')
    if imagename is not None and ".gif" in imagename:
      display['imagepath'] = 'images/' + imagename
    else:
      display['imagepath'] = ''
 
    display['text'] = request.json.get('text')
    display['textcolor'] = request.json.get('textcolor')
    display['bgcolor'] = request.json.get('bgcolor')
    display['scroll'] = request.json.get('scroll')
    display['blink'] = request.json.get('blink')
    print("text: " + display['text'])
    contentdisplayer.display(display['imagepath'], display['text'], display['textcolor'], display['bgcolor'], display['scroll'], display['blink'])
    return jsonify(display), 201

def beforeKill(*args):
  print "Kill requested"
  contentdisplayer.stop()
  sys.exit(0)

for sig in (SIGABRT, SIGINT, SIGTERM):
  signal(sig, beforeKill)

if __name__ == '__main__':
  app.run(debug = False, host = '127.0.0.1', threaded = False, use_reloader = False)
