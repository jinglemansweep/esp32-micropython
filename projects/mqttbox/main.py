import time
time.sleep(2)

import gc
import uasyncio as asyncio
from machine import Pin
from lib.mqttas import MQTTClient, config
from lib.stepper import create_stepper

from config import led_power, led_wifi, led_mqtt_connect, led_mqtt_msg, motor_i1, motor_i2, motor_i3, motor_i4

gc.collect()

SLEEP_SECS = 0.001
TOPIC = 'test'

motor = create_stepper(motor_i1, motor_i2, motor_i3, motor_i4, delay=2)
motor.reset()

outages = 0

async def pulse():
    led_mqtt_msg(True)
    await asyncio.sleep(1)
    led_mqtt_msg(False)

def on_message(topic, msg, retained):
    print(f'Topic: "{topic.decode()}" Message: "{msg.decode()}" Retained: {retained}')
    asyncio.create_task(pulse())

async def handle_wifi(state):
    global outages
    led_wifi(not state)
    if state:
        print('Status: Connected')
    else:
        outages += 1
        print('Status: Not Connected')
    await asyncio.sleep(1)

async def handle_connection(client):
    await client.subscribe('foo_topic', 1)

async def main(client):
    try:
        await client.connect()
    except OSError:
        print('Status: Connection Failed')
        return
    n = 0
    while True:
        await asyncio.sleep(5)
        print('publish', n)
        await client.publish(TOPIC, '{} repubs: {} outages: {}'.format(n, client.REPUB_COUNT, outages), qos = 1)
        n += 1

config['subs_cb'] = on_message
config['wifi_coro'] = handle_wifi
config['will'] = (TOPIC, 'GOODBYE', False, 0)
config['connect_coro'] = handle_connection
config['keepalive'] = 120

MQTTClient.DEBUG = True
client = MQTTClient(config)

try:
    asyncio.run(main(client))
finally:  # Prevent LmacRxBlk:1 errors.
    client.close()
    led_mqtt_msg(True)
    asyncio.new_event_loop()

