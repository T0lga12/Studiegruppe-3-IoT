import _thread
#Table of context:
#6 - 13 imported libary
#14 - 33 Global Variables
#33 - 37 Clear Neo ring
#39 - 62 Start Neoring
#63 - 95 Adafruit GPS

import umqtt_robust2 as mqtt
from machine import Pin,ADC
from time import sleep
from machine import PWM
import adafruit_gps_main
import tm1637
import neopixel

analog_pin = ADC(Pin(34))
analog_pin.atten(ADC.ATTN_11DB)
analog_pin.width(ADC.WIDTH_12BIT)

p = 15
n = 12

np = neopixel.NeoPixel(Pin(p), n)

Tilt = Pin(17, Pin.IN)
counter = 0

first = Tilt.value()
sleep(0.1)
second = Tilt.value()

tm = tm1637.TM1637(clk=Pin(18), dio=Pin(19))

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
        
        #print("TEST LOOP1")
        if first == 1 and second == 0:
            print("TEST LYS")
            counter += 1
            if counter >= 1 and counter < 12:
                for i in range(counter):
                    np[i] = (0, 170, 0)
                    np.write()
            if counter >= 12:
                for i in range(n):
                    np[i] = (170, 0, 0)
                    np.write()
            sleep(2)

clear_neopixel()
_thread.start_new_thread(tilt_neopixel, ())

while True:
    try:
        # Jeres kode skal starte her
        
        #batteri
        analog_val = analog_pin.read()
        volts = (analog_val * 0.000350545)*5
        battery_percentage = volts*100 - 320
        print("Volt:", volts, "v")
        print("The Batter percentage is:", battery_percentage / 3, "%")
        realBattery = battery_percentage / 3
        realBattery
        
        mqtt.web_print(battery_percentage / 3, 'Tolga12/feeds/Min Feed/csv') #Vigtig for feed/dashboard
        tm.number(int(realBattery))
        sleep(4)

        #GPS       
        adafruit_gps_main.GPS() #Husk det er den grønne ledning ú
    
           
        # Jeres kode skal slutte her
        sleep(0.5)
        if len(mqtt.besked) != 0: # Her nulstilles indkommende beskeder
            mqtt.besked = ""            
        mqtt.sync_with_adafruitIO() # igangsæt at sende og modtage data med Adafruit IO             
        print(".", end = '') # printer et punktum til shell, uden et enter        
    # Stopper programmet når der trykkes Ctrl + c
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()

