import umqtt_robust2 as mqtt
from machine import Pin,ADC
from time import sleep

analog_pin = ADC(Pin(34))
analog_pin.atten(ADC.ATTN_11DB)
analog_pin.width(ADC.WIDTH_12BIT)

while True:
    try:
        analog_val = analog_pin.read()
        volts = (analog_val * 0.00094638)*5
        battery_percentage = volts*100 - 320
        print("Volt:", volts, "v")
        print("The Batter percentage is:", battery_percentage / 2, "%")
        
        mqtt.web_print(battery_percentage / 2)
        
        sleep(0.5)
        if len(mqtt.besked) != 0:
            mqtt.besked = ""
        mqtt.sync_with_adafruitIO()
        print(".", end = '')
        
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()
    
        