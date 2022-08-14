import time
from machine import Pin
import gc

from utils import wifi_connect, reboot, flash_pin
from messaging import mqtt_connect
from lib.stepper import create_stepper

gc.collect()

# Useful constants
SLEEP_SECS = 0.001

# Pin definitions
pin_led_power = Pin(21, Pin.OUT)
pin_led_wifi = Pin(22, Pin.OUT)
pin_led_mqtt_connect = Pin(23, Pin.OUT)
pin_led_mqtt_message = Pin(15, Pin.OUT)
pin_motor_i1 = Pin(26, Pin.OUT)
pin_motor_i2 = Pin(25, Pin.OUT)
pin_motor_i3 = Pin(33, Pin.OUT)
pin_motor_i4 = Pin(32, Pin.OUT)

motor = create_stepper(pin_motor_i1, pin_motor_i2, pin_motor_i3, pin_motor_i4, delay=2)
motor.reset()

# Utility functions
def reset():
    pin_led_power(False)
    pin_led_wifi(False)
    pin_led_mqtt_connect(False)
    pin_led_mqtt_message(False)
    time.sleep(1)

# Reset all pins to boot state
reset()
pin_led_power(True)

# Attempt WiFi connection
wifi_connect(status_pin=pin_led_wifi)

# MQTT Callbacks
def on_message(topic, msg):
    print("{0}: {1}".format(topic, msg))
    flash_pin(pin_led_mqtt_message)
    try:
        if topic == b'esp32/dev/motor/command':
            on_command_motor(int(msg))
    except Exception as e:
        print(e)

def on_command_motor(payload):
    print("Motor Command: {0}".format(payload))
    motor.angle(int(payload))
    
mqtt_client = mqtt_connect(b'esp32/dev/motor/#', on_message, pin_led_mqtt_connect)

# Main Loop
print("Main Loop")
while True:
    try:
        mqtt_client.check_msg()
    except Exception as e:
        print("MQTT Error", e)
    time.sleep(SLEEP_SECS)
    
            
        

