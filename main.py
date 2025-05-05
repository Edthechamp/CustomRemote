import paho.mqtt.client as mqtt
import subprocess
print("Starting MQTT client...")

def on_connect(client, userdata, flags, rc):
    print("connected")
    client.subscribe("home/media")
    client.subscribe("controls/basic")

#for windows
def message(client, userdata, msg):
    command = msg.payload.decode()
    if msg.topic == "home/media":
        media(command)
    elif msg.topic == "controls/basic":
        controls(command)

def media(command):
    if command == "netflix":
        print("Opening Netflix")
        subprocess.run(['firefox','-kiosk','netflix.com'])
    elif command == "youtube":
        print("Opening YouTube")
        subprocess.run(['firefox',"https://www.youtube.com"])

def controls(command):
    subprocess.run(['xdotool', 'key', command])
    print(f"Key {command} pressed")

#publishing client is phone with mqtt app

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = message

client.connect("192.168.23.105", 1883, 60)
client.loop_forever()
