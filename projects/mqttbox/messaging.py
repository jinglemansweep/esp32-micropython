import machine
import ubinascii
from lib.umqttsimple import MQTTClient
from utils import reboot

from secrets import MQTT_HOST, MQTT_PORT, MQTT_SSL, MQTT_CLIENT_ID, MQTT_USERNAME, MQTT_PASSWORD

MQTT_KEEPALIVE = 60

def build_client(topic, cb):
    client_id = ubinascii.hexlify(machine.unique_id())
    client = MQTTClient(client_id, MQTT_HOST, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD, MQTT_KEEPALIVE, MQTT_SSL)
    client.set_callback(cb)
    client.connect()
    client.subscribe(topic)
    return client

def mqtt_connect(topic, cb, status_pin):
    print('MQTT Connecting...')
    try:
        client = build_client(topic, cb)
    except Exception as e:
        print("Error", e)
        reboot('MQTT connection failed, restarting...')
    print('MQTT Connected')
    if status_pin: status_pin(True)
    return client

