from modules import ws2812
from fpioa_manager import *
class_ws2812 = ws2812(8,100)
r=0
dir = True
while True:
    if dir:
        r += 5
    else:
        r -= 5
    if r>=255:
        r = 255
        dir = False
    elif r<0:
        r = 0
        dir = True
    for i in range(100):
        a = class_ws2812.set_led(i,(0,0,r))
    a=class_ws2812.display()