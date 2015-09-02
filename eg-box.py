#!/usr/bin/env python3
# basic moving box

import turtle
import engine
import random
import math
import time

WIDTH = 640
HEIGHT = 480
speed = 0
xspeed = 0
lost = False

class Box(engine.GameObject):
	def __init__(self):
		super().__init__(0, 0, 0, 0, 'fusee', 'red')
	def move(self):
		#self.x += 2
		#self.y += 1
		# with the following code we get the frantic move we expected
		#self.x += random.randrange(-1,2)
		#self.y += random.randrange(-1,2)
		global speed
		global xspeed
		global lost
		if self.y >= 165:
			speed = 0
			if lost == False:
				banner("Burnt!")
				lost = True
		elif self.y > (-230 + speed) or speed < 0:
			self.y -= speed
			speed += 0.02
		else:
			if abs(speed) > 3:
				banner("Crashed!")
				lost = True
			self.y = -230
			speed = 0
		#self.x += xspeed
		#if xspeed != 0:
			#xspeed = math.exp(-1 * abs(xspeed)) * xspeed / abs(xspeed)

def keyboard_cb(key):
	global speed
	global xspeed
	if key == 'space':
		if lost == False:
			speed -= 0.2
	elif key == 'Escape':
		print("Au revoir...")
		engine.exit_engine()
	elif key == 'Left':
		xspeed -= 0.1
	elif key == 'Right':
		xspeed += 0.1
	else:
		print(key)

def drawfus(): # spaceship!
	B = 15
	turtle.begin_poly()
	turtle.fd(B)
	turtle.rt(90)
	turtle.fd(B)
	turtle.rt(90)
	turtle.fd(B)
	turtle.rt(90)
	turtle.fd(B)
	turtle.fd(2.25 * B)
	turtle.rt(90)
	turtle.fd(B)
	turtle.rt(90)
	turtle.fd(B)
	turtle.rt(90)
	turtle.fd(B)
	turtle.fd(3 * B)
	turtle.rt(-90)
	turtle.fd(1.25 * B)
	
	turtle.end_poly()
	poly = turtle.get_poly() # c'est le poly... yveslemaire.poly
	turtle.register_shape('fusee', poly)

def banner(s):
	turtle.home()
	turtle.color('black')
	turtle.write(s, True, align='center', font=('Arial', 48, 'italic'))
	time.sleep(3)
	turtle.undo()


def drawsun():
	turtle.setposition(0, 240)
	turtle.dot(150, 'yellow')

if __name__ == '__main__':
	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine()
	engine.set_keyboard_handler(keyboard_cb)
	drawfus()
	drawsun()
	box = Box()
	engine.add_obj(box)
	engine.engine()

