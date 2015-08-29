#!/usr/bin/env python

import collections
import time
import bluetooth
import sys
import subprocess
import math
import time
import json
import Adafruit_GPIO as GPIO
import Adafruit_CharLCD as LCD
import paho.mqtt.client as mqtt
from wiiboard import Wiiboard
from lcd import Plate
import os
config_file = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "settings.json")
with open(config_file) as f:
    config = json.load(f)
    users = config["users"]
    board_address = config["address"]
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(config["broker"]["host"], config["broker"].get("port", 1883), 60)
# Initialize the LCD using the pins 
lcd = Plate()

def main():
    board = Wiiboard()
    lcd.set_backlight(True)
    lcd.clear()
    lcd.message("Trying to \nconnect...")
    lcd.trigger_sync_mode()
    try:
        board.connect(board_address)  # The wii board must be in sync mode at this time
    except bluetooth.btcommon.BluetoothError:
        lcd.clear()
        lcd.message("Connecting failed")
        time.sleep(2)
        return
    time.sleep(0.2)
    user = lcd.run_menu(users)
    lcd.clear()
    lcd.message("Step on the \nboard")
    board.receive()
    lcd.clear()
    if config["unit"] == "lb":
    	lcd.message("You weigh %.1flb" % (float(board.weight) * 2.20462))
    	client.publish("/weight", json.dumps({
        	"weight":float(board.weight) * 2.20462,
        	"unit":"lb",
		"owner":user.get("userID", ""),
    	}))
    elif config["unit"] == "kg":
	lcd.message("You weigh %.1fkg" % board.weight)
        client.publish("/weight", json.dumps({
                "weight":float(board.weight),
                "unit":"kg",
                "owner":user.get("userID", ""),
        }))
    time.sleep(5)
if __name__ == "__main__":
    client.loop_start()    
    start = time.time()
    lcd.set_backlight(True)
    lcd.clear()
    lcd.message("Hello!\nPress a button...")
    while True:
	
        if lcd.is_pressed(LCD.SELECT) or lcd.is_pressed(LCD.DOWN) or lcd.is_pressed(LCD.UP) or lcd.is_pressed(LCD.LEFT) or lcd.is_pressed(LCD.RIGHT):
            main()
            lcd.clear()
            lcd.message("Hello!\nPress a button.")
	    start = time.time()
	    lcd.set_backlight(True)
	if (time.time() - start) > 20:
		lcd.set_backlight(False)
