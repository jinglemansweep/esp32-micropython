import time
from machine import Pin
import gc

from utils import wifi_connect, reboot, flash_pin
from messaging import mqtt_connect

gc.collect()

# Useful constants
SLEEP_SECS = 0.001

# Pin definitions
pin_led_power = Pin(21, Pin.OUT)
pin_led_wifi = Pin(22, Pin.OUT)
pin_led_mqtt_connect = Pin(23, Pin.OUT)
pin_led_mqtt_message = Pin(15, Pin.OUT)

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

mqtt_client = mqtt_connect(b'test/hello', on_message, pin_led_mqtt_connect)

# Main Loop
print("Main Loop")
while True:
    #try
    mqtt_client.check_msg()
    time.sleep(SLEEP_SECS)
    #except Exception as e:
    #    reboot('Main loop crashed, restarting...')

            
        

