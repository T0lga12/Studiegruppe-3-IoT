import umqtt_robust2 as mqtt
from machine import Pin,ADC
from time import sleep
from machine import PWM
import adafruit_gps_main
import tm1637
import neopixel
import _thread

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


# Her kan i placere globale varibaler, og instanser af klasser
# instans af Pin klassen AKA et Pin objekt
tm = tm1637.TM1637(clk=Pin(2), dio=Pin(4))

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
        
        print("TEST LOOP1")
        if first == 1 and second == 0:
            print("TEST LYS")
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

while True:
    print("TEST LOOP2")
    try:
        # Jeres kode skal starte her

        #batteri
        analog_val = analog_pin.read()
        volts = (analog_val * 0.00095545)*5
        battery_percentage = volts*100 - 320
        print("Volt:", volts, "v")
        print("The Batter percentage is:", battery_percentage / 2, "%")
        realBattery = battery_percentage / 2
        
        mqtt.web_print(battery_percentage / 2, 'Tolga12/feeds/Min Feed/csv') #Vigtig for feed/dashboard
        tm.number(int(realBattery))
        sleep(4)

        #GPS       
        adafruit_gps_main.GPS()
    
           
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
