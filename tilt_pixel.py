from machine import Pin
from time import sleep
import neopixel
import time
import _thread

p = 15
n = 12

np = neopixel.NeoPixel(Pin(p), n)

Tilt = Pin(17, Pin.IN)
counter = 0

def clear_neopixel():
    for i in range(n):
        np[i] = (0, 0, 0)
        np.write()

def tilt_neopixel():
    while True:
        first = Tilt.value()
        sleep(0.1)
        second = Tilt.value()
        global counter 

        if first == 1 and second == 0:
            print("test")
            counter += 1
            if counter >= 1:
                for i in range(counter):
                    np[i] = (0, 170, 0)
                    np.write()
            if counter >= 12:
                for i in range(n):
                    np[i] = (170, 0, 0)
                    np.write()
            sleep(5)

clear_neopixel()

_thread.start_new_thread(tilt_neopixel, ())
