
import time
import machine
import network
import webrepl

from secrets import WIFI_SSID, WIFI_KEY

LED_FLASH_SPEED = 0.1

def flash_pin(pin, delay=LED_FLASH_SPEED):
    pin(True)
    time.sleep(delay)
    pin(False)

def wifi_connect(status_pin=None):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('WiFi Connecting...')
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_KEY)
        while not sta_if.isconnected():
            if status_pin: flash_pin(status_pin)
            pass
    if status_pin: status_pin(True)
    webrepl.start()
    print('WiFi Connected', sta_if.ifconfig())

def reboot(msg='Restarting...', delay=5):
    print(msg)
    time.sleep(delay)
    machine.reset()