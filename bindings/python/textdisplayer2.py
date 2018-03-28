#!/usr/bin/env python
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

class textdisplayer():

  def __init__(self):
    # Configuration for the matrix
    options = RGBMatrixOptions()
    options.cols = 64
    options.rows = 32
    options.chain_length = 1
    options.parallel = 1
    options.gpio_slowdown = 2
    options.hardware_mapping = 'adafruit-hat'

    self.matrix = RGBMatrix(options = options)
    self.font = graphics.Font()
    self.font.LoadFont("../../fonts/9x18.bdf")
    #self.textColor = graphics.Color(0, 0, 255)
    self.offscreen_canvas = self.matrix.CreateFrameCanvas()
    print("init done")

  def displayText(self, text, textcolor, bgcolor, scroll, blink):
    pos = self.offscreen_canvas.width
    print("text: " + text)
	clearDisplay();
	setBg(graphics.Color(bgcolor[0], bgcolor[1], bgcolor[2]));
    graphics.DrawText(self.offscreen_canvas, self.font, 0, 28, graphics.Color(textcolor[0], textcolor[1], textcolor[2]), text)

    self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

  def clearDisplay(self):
    self.offscreen_canvas.Clear()
	
  def setBg(self, bgcolor):
    for y in range(0, options.rows):
	  graphics.DrawLine(self.offscreen_canvas, 0, y, options.cols, y, bgcolor):

if __name__ == "__main__":
  disp = textdisplayer()
  disp.clearDisplay()
  #disp.displayText("Go Vikings", 0)
  time.sleep(5)

