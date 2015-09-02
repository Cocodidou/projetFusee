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
countreac = 0
basesize = 15
sundiam = 150

class Box(engine.GameObject):
	def __init__(self):
		super().__init__(0, 0, 0, 0, 'fusee', 'black')
	def move(self):
		#self.x += 2
		#self.y += 1
		# with the following code we get the frantic move we expected
		#self.x += random.randrange(-1,2)
		#self.y += random.randrange(-1,2)
		global speed
		global xspeed
		global lost
		global box
		global countreac
		if self.y >= HEIGHT / 2. - sundiam:
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
		countreac += 1
		if countreac > 20:
			box.color = "black"
		#self.x += xspeed
		#if xspeed != 0:
			#xspeed = math.exp(-1 * abs(xspeed)) * xspeed / abs(xspeed)

def keyboard_cb(key):
	global speed
	global xspeed
	global box
	global countreac
	if key == 'space':
		if lost == False:
			speed -= 0.2
			box.color = "red"
			countreac = 0
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
	global basesize
	B = basesize
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
	global sundiam
	turtle.setposition(0, 240)
	turtle.dot(sundiam, 'yellow')

def drawground():
	s = turtle.Shape("compound")
	ground = ((-320, 120), (-280, 41), (-240, 27),
		   (-200, 59), (-160, 25), (-120, 43), (-80, 56),
		   (-40, 20), (0, 20), (40, 20), (80, 44),
		(120, 28), (160, 66), (200, 29), (240, 64),
		(280, 34), (320, 140), (320, 0), (-320,0) ) 
	s.addcomponent(ground, "black", "black")
	turtle.register_shape('ground', s)
	#turtle.

if __name__ == '__main__':
	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine()
	engine.set_keyboard_handler(keyboard_cb)
	drawfus()
	drawsun()
	drawground()
	box = Box()
	engine.add_obj(box)
	engine.engine()

