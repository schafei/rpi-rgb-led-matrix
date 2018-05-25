#!/usr/bin/env python
import time
import sys
import threading
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image

class DisplayerThread(threading.Thread):

  stopFlag = False

  def __init__(self, canvas, matrix, imagepath, text, textcolor, bgcolor, scroll, blink):
    super(DisplayerThread, self).__init__()
    self.canvas=canvas
    self.matrix=matrix
    self.imagepath=imagepath
    self.text=text
    self.textcolor=textcolor
    self.bgcolor=bgcolor
    self.scroll=scroll
    self.blink=blink
	
    self.font = graphics.Font()
    self.font.LoadFont("../../fonts/helvR12.bdf")

  def run(self):
    self.clearDisplay()
    count=0
    #needed for scrolling, set x textposition to right end of display
    xtxtposition = self.canvas.width
    #default y textposition without picture
    ytxtposition = 20

    while(not self.stopFlag):
      if (self.blink and count%2==1):
        self.setBg(graphics.Color(0, 0, 0))
      else: 
        self.setBg(graphics.Color(int(self.bgcolor[0]), int(self.bgcolor[1]), int(self.bgcolor[2])))
      
      if (len(self.imagepath) > 0):
        image = Image.open(self.imagepath)
        imgheigth, imgwidth = image.size
        thumbnailheigth = 20
        ratio = imgheigth / float(thumbnailheigth)
        thumbnailwidth = int(imgwidth / ratio)
        image.thumbnail((thumbnailheigth, thumbnailwidth), Image.ANTIALIAS)
        self.matrix.SetImage(image.convert('RGB'), (self.canvas.width / 2 - thumbnailwidth / 2), 0)
#        print ("Ratio: " + str(ratio) + ", Image: " + str(imgwidth) + "x" + str(imgheigth) + ", Thumbnail: " + str(thumbnailwidth) + "x" + str(thumbnailheigth))
        #change y textposition to the lowest possible
        ytxtposition = 29
      
      if (self.scroll):
        length = graphics.DrawText(self.canvas, self.font, xtxtposition, ytxtposition, graphics.Color(int(self.textcolor[0]), int(self.textcolor[1]), int(self.textcolor[2])), self.text)
        xtxtposition -= 1
        if (xtxtposition + length < 0 ):
          xtxtposition = self.canvas.width
      else: 
        graphics.DrawText(self.canvas, self.font, 0, ytxtposition, graphics.Color(int(self.textcolor[0]), int(self.textcolor[1]), int(self.textcolor[2])), self.text)

      time.sleep(0.1)
      self.canvas = self.matrix.SwapOnVSync(self.canvas)
      count += 1
    self.clearDisplay()
  
  def setStopFlag(self, stopFlag):
    self.stopFlag = stopFlag
	
  def clearDisplay(self):
    self.canvas.Clear()
	
  def setBg(self, bgcolor):
    for y in range(0, self.canvas.height):
      graphics.DrawLine(self.canvas, 0, y, self.canvas.width, y, bgcolor)
    
class contentdisplayer():

  width = 32
  cols = 64
  thread = None

  def __init__(self):
    # Configuration for the matrix
    options = RGBMatrixOptions()
    options.cols = self.cols
    options.rows = self.width
    options.chain_length = 1
    options.parallel = 1
    options.gpio_slowdown = 2
    options.hardware_mapping = 'adafruit-hat'
    options.pwm_lsb_nanoseconds = 250 
    self.matrix = RGBMatrix(options = options)

    self.offscreen_canvas = self.matrix.CreateFrameCanvas()
    print("init done")

  def display(self, imagepath, text, textcolor, bgcolor, scroll, blink):
    #print("text: " + text)
    if (self.thread != None):
      self.thread.setStopFlag(True)
      self.thread.join()
      self.thread = None
    self.thread = DisplayerThread(self.offscreen_canvas, self.matrix, imagepath, text, textcolor, bgcolor, scroll, blink)
    self.thread.daemon = True
    self.thread.start()

  def stop(self):
    #print("stop called")
    if (self.thread != None):
      self.thread.setStopFlag(True)
      self.thread.join()

if __name__ == "__main__":
  disp = contentdisplayer()
  disp.display("", "Go Vikings", [255,0,0], [255,255,255], 'true', 'false')
  time.sleep(5)


