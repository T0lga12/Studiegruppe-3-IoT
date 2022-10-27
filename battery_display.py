import tm1637
import umqtt_robust2 as mqtt
from machine import Pin
from time import sleep, sleep

tm = tm1637.TM1637(clk=Pin(2), dio=Pin(4))

def batteryDisplay():
    analog_val = analog_pin.read()
    volts = (analog_val * 0.00094638)*5
    battery_percentage = volts*100 - 320
    print("Volt:", volts, "v")
    print("The Batter percentage is:", battery_percentage / 2, "%")
    realBattery = battery_percentage / 2
        
    mqtt.web_print(battery_percentage / 2, 'Tolga12/feeds/Min Feed/csv') #Vigtig for feed/dashboard
    sleep(4)

    tm.number(int(realBattery))
    sleep(1)