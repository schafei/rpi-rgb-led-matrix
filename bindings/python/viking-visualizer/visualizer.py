#!/usr/bin/env python
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

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
    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("../../../fonts/7x13.bdf")
    textColor = graphics.Color(255, 255, 0)
    pos = offscreen_canvas.width

    while True:
        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, "Hello Vikings")
        pos -= 1
        if (pos + len < 0):
            pos = offscreen_canvas.width

        time.sleep(0.05)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
        
except KeyboardInterrupt:
    sys.exit(0)
