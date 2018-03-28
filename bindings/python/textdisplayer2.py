#!/usr/bin/env python
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

class textdisplayer():

  width = 32
  cols = 64

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
    self.font = graphics.Font()
    self.font.LoadFont("../../fonts/helvR12.bdf")
    #self.textColor = graphics.Color(0, 0, 255)
    self.offscreen_canvas = self.matrix.CreateFrameCanvas()
    print("init done")

  def displayText(self, text, textcolor, bgcolor, scroll, blink):
    pos = self.offscreen_canvas.width
    print("text: " + text)
    self.clearDisplay()
    self.setBg(graphics.Color(int(bgcolor[0]), int(bgcolor[1]), int(bgcolor[2])))
    graphics.DrawText(self.offscreen_canvas, self.font, 0, 20, graphics.Color(int(textcolor[0]), int(textcolor[1]), int(textcolor[2])), text)

    self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

  def clearDisplay(self):
    self.offscreen_canvas.Clear()
	
  def setBg(self, bgcolor):
    for y in range(0, self.width):
      graphics.DrawLine(self.offscreen_canvas, 0, y, self.cols, y, bgcolor)

if __name__ == "__main__":
  disp = textdisplayer()
  disp.clearDisplay()
  disp.displayText("Go Vikings", [255,0,0], [255,255,255], 'true', 'false')
  time.sleep(5)

