import paho.mqtt.client as mqtt
import webbrowser
print("Starting MQTT client...")

def on_connect(client, userdata, flags, rc):
    print("connected")
    client.subscribe("home/media")


def message(client, userdata, msg):
    command = msg.payload.decode()
    print(f"Received command: {command}")
    if command == "netflix":
        print("Opening Netflix")
        webbrowser.open("https://www.netflix.com")
        #replace iwth launch script on linux
    elif command == "youtube":
        print("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
        #replace iwth launch script on linux
        

#publishing client is phone with mqtt app

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = message

client.connect("192.168.23.105", 1883, 60)
client.loop_forever()
