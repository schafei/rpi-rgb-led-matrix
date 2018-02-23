#!/usr/bin/env python
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

content = [ '', '']

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
    self.font.LoadFont("../../fonts/helvR12.bdf")
    self.textColor = graphics.Color(0, 0, 255)
    self.offscreen_canvas = self.matrix.CreateFrameCanvas()
    print("init done")

  def displayText(self, text, line):
    pos = self.offscreen_canvas.width
    content[line] = text
    print("text: " + text + " line: " + str(line) + " pos: " + str(pos))
    graphics.DrawText(self.offscreen_canvas, self.font, 0, 14, self.textColor, content[0])
    graphics.DrawText(self.offscreen_canvas, self.font, 0, 29, self.textColor, content[1])

    self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

  def clearDisplay(self):
    self.offscreen_canvas.Clear()

if __name__ == "__main__":
  disp = textdisplayer()
  disp.clearDisplay()
  disp.displayText("Go Vikings", 0)
  disp.displayText("----------", 1)
  time.sleep(5)

