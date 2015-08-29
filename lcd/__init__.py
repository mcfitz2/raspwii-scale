from Adafruit_CharLCD import Adafruit_CharLCDPlate
import Adafruit_GPIO as GPIO
import Adafruit_CharLCD as LCD

import time
class Plate(Adafruit_CharLCDPlate):
	def __init__(self):
		Adafruit_CharLCDPlate.__init__(self)
		self._gpio.setup(5, GPIO.OUT)

	def draw_list(self, items, index, height=2):
		self.clear()
		self.message("> %s\n %s" % (items[index]["name"], items[(index+1) % (len(items) -1)]["name"]))
	def trigger_sync_mode(self):
		self._gpio.output(5, GPIO.HIGH)
		time.sleep(0.1)
		self._gpio.output(5, GPIO.LOW) 
	def run_menu(self, users):
		index = 0
		self.draw_list(users, index)
		while True:
			if self.is_pressed(LCD.DOWN):
				index = (index + 1) % (len(users))
				self.draw_list(users, index)   
			elif self.is_pressed(LCD.UP):
				if (index - 1) < 0:
					index = len(users) - 1 
				else:
					index -= 1 
				self.draw_list(users, index)  
			elif self.is_pressed(LCD.SELECT):
				self.clear()
				self.message("Hello, %s!" % users[index]["name"])
				time.sleep(0.5)
				return users[index]
