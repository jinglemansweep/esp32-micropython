from machine import Pin, PWM 
import network
import webrepl

import random
import time

from stepper import create_stepper
from secrets import WIFI_SSID, WIFI_KEY

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_KEY)
    while not sta_if.isconnected():
        pass
print('network config:', sta_if.ifconfig())

webrepl.start()

SLEEP_SECS = 0.001

pin_led_status = Pin(15, Pin.OUT)
pin_led_r = Pin(21, Pin.OUT)
pin_led_g = Pin(22, Pin.OUT)
pin_led_b = Pin(23, Pin.OUT)

pwm_led_r = PWM(pin_led_r, 5000)
pwm_led_g = PWM(pin_led_g, 5000)
pwm_led_b = PWM(pin_led_b, 5000)

pin_led_status(False)

pin_motor_i1 = Pin(26, Pin.OUT)
pin_motor_i2 = Pin(25, Pin.OUT)
pin_motor_i3 = Pin(33, Pin.OUT)
pin_motor_i4 = Pin(32, Pin.OUT)

motor = create_stepper(pin_motor_i1, pin_motor_i2, pin_motor_i3, pin_motor_i4, delay=2)

direction = 1 # clockwise (-1 for anti-clockwise)
step = 0

print("Main Loop")
while True:
    for cycle in range(0, 1024):
        # LEDs
        pwm_led_r.duty(cycle)
        pwm_led_g.duty(1023-cycle)
        pwm_led_b.duty(int(cycle/10))
        # Motor
        
        motor.step(direction)
        step = step + direction
        
        if step >= motor.FULL_ROTATION:
            step = 0
            direction = 0 - direction
        
        print("Step: {0} | Direction: {1}".format(step, direction))
        time.sleep(SLEEP_SECS)
        
        

