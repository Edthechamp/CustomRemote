import paho.mqtt.client as mqtt
import subprocess
print("Starting MQTT client..")

def on_connect(client, userdata, flags, rc):
    print("connected")
    client.subscribe("home/media")
    client.subscribe("controls/basic")
    client.subscribe("controls/power")
    print("subscribed to topics")


def message(client, userdata, msg):
    command = msg.payload.decode()
    if msg.topic == "home/media":
        media(command)
    elif msg.topic == "controls/basic":
        controls(command)
    elif msg.topic == "controls/power":
        power(command)
    #TODO: add spotify support not sure how to go about it yet, i want the tv to just display lyrics, but audio play frmo phone, to avoid having to switch bluetooth headphone connection

def media(command):
    if command == "netflix":
        print("Opening Netflix")
        subprocess.run(['firefox','-kiosk','netflix.com']) #kiosk mode is slightly buggy, doesnt allow other input until closed and doesnt work if firefox is already open
        #TODO: check if netflix is already open and swithc focus in that case and add a way to close it once done
    elif command == "youtube":
        print("Opening YouTube")
        subprocess.run(['firefox',"https://www.youtube.com"])
        #TODO: same as netflix


def controls(command):
    subprocess.run(['xdotool', 'key', command])
    print(f"Key {command} pressed")
    #donsnt really work as expected, just scrolls instead of selecting things like a smartTV, likely need to rewrite with selenium for proper navigation. or maybe use KODI on linux system instead of firefox, but then DRM might cause problems

def power(command): #linux machine stasy on,but toggles display output(hoping an idle machine with no display has low power consumption). My system BIOS doesnt support wake on lan, wake on AC power or wake on USB, so this is the only solution i could think of
    if command == "on":
        subprocess.run(['xrandr', '--output', 'HDMI-1', '--auto'])
        
        #for better performence maybe preload firefox browser here as well, might do later
    elif command == "off":
        subprocess.run(['xrandr', '--output', 'HDMI-1', '--off'])
    #no need to check if is on/off, because publishing client takes care of that


#publishing client is phone with an mqtt app
#server is a mosquitto broker on the same machine as the client

#TODO: maybe replace subprocess.run with prebiuilt executable built for better performance

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = message

client.connect("localhost", 1883, 60)
client.loop_forever()
