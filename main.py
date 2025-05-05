import paho.mqtt.client as mqtt
import subprocess
print("Starting MQTT client...")

def on_connect(client, userdata, flags, rc):
    print("connected")
    client.subscribe("home/media")
    client.subscribe("controls/basic")


def message(client, userdata, msg):
    command = msg.payload.decode()
    if msg.topic == "home/media":
        media(command)
    elif msg.topic == "controls/basic":
        controls(command)
    #TODO: add spotify support

def media(command):
    if command == "netflix":
        print("Opening Netflix")
        subprocess.run(['firefox','-kiosk','netflix.com'])
        #TODO: check if netflix is already open and swithc focus in that case and add a way to close it once done
    elif command == "youtube":
        print("Opening YouTube")
        subprocess.run(['firefox',"https://www.youtube.com"])
        #TODO: same as netflix


def controls(command):
    subprocess.run(['xdotool', 'key', command])
    print(f"Key {command} pressed")

#publishing client is phone with mqtt app

#TODO: maybe replace subprocess.run with prebiuilt executable for better performance

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = message

client.connect("localhost", 1883, 60) #subscribed client is on the same linux machine as the broker
client.loop_forever()
