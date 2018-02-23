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
    self.font.LoadFont("../../fonts/helvR12.bdf")
    self.textColor = graphics.Color(0, 0, 255)
    print("init done")
  def displayText(self, text, line):
    print("text:" + text)

    offscreen_canvas = self.matrix.CreateFrameCanvas()
    print("Create is done")
    pos = offscreen_canvas.width
   
    print("before loop") 
    while True:
        print("loop")
        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas, self.font, pos, 2 + line * 12, self.textColor, text)
        pos -= 1
        if (pos + len < 0):
            pos = offscreen_canvas.width

        time.sleep(0.05)
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
