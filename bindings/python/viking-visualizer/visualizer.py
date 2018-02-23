#!/usr/bin/env python
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

def displaytext(text, matrix, font, line, textColor):
    offscreen_canvas = matrix.CreateFrameCanvas()
    pos = offscreen_canvas.width
    
    while True:
        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas, font, pos, 2 + line * 12, textColor, text)
        pos -= 1
        if (pos + len < 0):
            pos = offscreen_canvas.width

        time.sleep(0.05)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)


# Configuration for the matrix
options = RGBMatrixOptions()
options.cols = 64
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.gpio_slowdown = 2
options.hardware_mapping = 'adafruit-hat'

matrix = RGBMatrix(options = options)

try:
    print("Press CTRL-C to stop.")
    
    font = graphics.Font()
    font.LoadFont("../../../fonts/helvR12.bdf")
    textColor = graphics.Color(0, 0, 255)
    displayText("Hello Vikings", matrix, font, 1, textColor)
        
except KeyboardInterrupt:
    sys.exit(0)
