import umqtt_robust2 as mqtt
from machine import Pin,ADC
from time import sleep
from machine import PWM
import adafruit_gps_main

analog_pin = ADC(Pin(34))
analog_pin.atten(ADC.ATTN_11DB)
analog_pin.width(ADC.WIDTH_12BIT)


# Her kan i placere globale varibaler, og instanser af klasser
red_LED = Pin(15, Pin.OUT) # instans af Pin klassen AKA et Pin objekt
B_PIN = 25
buzzer = PWM(Pin(B_PIN, Pin.OUT),duty=0)

while True:
    try:        
        # Jeres kode skal starte her
    #batteri
        analog_val = analog_pin.read()
        volts = (analog_val * 0.00094638)*5
        battery_percentage = volts*100 - 320
        print("Volt:", volts, "v")
        print("The Batter percentage is:", battery_percentage / 2, "%")
        
        mqtt.web_print(battery_percentage / 2, 'Tolga12/feeds/Min Feed/csv') #Vigtig for feed/dashboard
        sleep(4)
        
    #batteri
    #GPS       
        adafruit_gps_main.GPS()  
           
        if mqtt.besked == "svar_tilbage":
            mqtt.web_Print("ESP32 her!")
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
