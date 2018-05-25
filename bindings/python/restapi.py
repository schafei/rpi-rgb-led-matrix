#!/usr/bin/env python
import sys
from flask import Flask, jsonify, request, render_template
from signal import *
from contentdisplayer import contentdisplayer

contentdisplayer = contentdisplayer()
mainRoute = '/display'
app = Flask(__name__, static_url_path = mainRoute)

#default: no image, white font on black bg, scrolling, not blinking
displayDefault = { 'imagepath': '', 'text': '', 'textcolor': ['255', '255', '255'], 'bgcolor': ['0', '0', '0'], 'scroll': 'true', 'blink': 'false' }
display = displayDefault

@app.route(mainRoute + '/', methods=['GET','POST','PUT','DELETE'])
def routing():

  if request.method == 'GET':
    jsonify(display)

  elif request.method == 'PUT':
    #text has to be set, all others are optional (see displayDefault)
    display = displayDefault
    display['text'] = request.json.get('text')
	
    #imagepath has priority, when imagepath and imagename are set
    imagename = request.json.get('imagename')
    if request.json.get('imagepath') is not None:
      display['imagepath'] = request.json.get('imagepath')
    elif imagename is not None and ".gif" in imagename:
      display['imagepath'] = 'images/' + imagename
	  
    if request.json.get('textcolor') is not None:
      display['textcolor'] = request.json.get('textcolor')
    if request.json.get('bgcolor') is not None:
      display['bgcolor'] = request.json.get('bgcolor')
    if request.json.get('scroll') is not None:
      display['scroll'] = request.json.get('scroll')
    if request.json.get('blink') is not None:
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
