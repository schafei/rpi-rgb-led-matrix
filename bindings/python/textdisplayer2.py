#!/usr/bin/env python
import time
import sys
import threading

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

class DisplayerThread(threading.Thread):

  stopFlag = False

  def __init__(self, canvas, matrix, text, textcolor, bgcolor, scroll, blink):
    super(DisplayerThread, self).__init__()
    self.canvas=canvas
    self.matrix=matrix
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
    pos = self.canvas.width
    while(not self.stopFlag):
      if (self.blink and count%2==1):
        self.setBg(graphics.Color(0, 0, 0))
      else: 
        self.setBg(graphics.Color(int(self.bgcolor[0]), int(self.bgcolor[1]), int(self.bgcolor[2])))
      
      if (self.scroll):
        len = graphics.DrawText(self.canvas, self.font, pos, 20, graphics.Color(int(self.textcolor[0]), int(self.textcolor[1]), int(self.textcolor[2])), self.text)
        pos -= 1
        if (pos + len < 0):
          pos = self.canvas.width
      else: 
        graphics.DrawText(self.canvas, self.font, 0, 20, graphics.Color(int(self.textcolor[0]), int(self.textcolor[1]), int(self.textcolor[2])), self.text)

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
    


class textdisplayer():

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

    self.matrix = RGBMatrix(options = options)

    self.offscreen_canvas = self.matrix.CreateFrameCanvas()
    print("init done")

  def displayText(self, imagepath, text, textcolor, bgcolor, scroll, blink):
    print("text: " + text)
    if (self.thread != None):
      self.thread.setStopFlag(True)
      self.thread.join()
      self.thread = None
    self.thread = DisplayerThread(self.offscreen_canvas, self.matrix, imagepath, text, textcolor, bgcolor, scroll, blink)
    self.thread.daemon = True
    self.thread.start()

if __name__ == "__main__":
  disp = textdisplayer()
  disp.displayText("Go Vikings", [255,0,0], [255,255,255], 'true', 'false')
  time.sleep(5)


