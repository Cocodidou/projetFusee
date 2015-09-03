#!/usr/bin/env python3
# basic moving ship

import turtle
import engine
import random
import math
import time

WIDTH = 640
HEIGHT = 480
speed = 0 # vitesse
countreac = 0 # compteur de frames du réacteur
basesize = 10
sundiam = 150
shiphead = 0 # tilt du vaisseau



xspeed = 0
yspeed = 0

class Ground(engine.GameObject):
	def __init__(self):
		super().__init__(0, -HEIGHT/2, 0, 0, 'ground', '#8B4513')
	def heading(self):
		return 90
	ground = ((-320, 120), (-280, 41), (-240, 27),
		(-200, 59), (-160, 25), (-120, 43), (-80, 56),
		(-40, 20), (0, 20), (40, 20), (80, 44),
	(120, 28), (160, 66), (200, 29), (240, 64),
	(280, 34), (320, 140), (320, 0), (-320,0) ) 

class Sun(engine.GameObject):
	def __init__(self):
		super().__init__(0, HEIGHT/2, 0, 0, 'sun', 'yellow')
		#super().__init__(0, 0, 0, 0, 'sun', 'yellow')

class Fusee(engine.GameObject):
	def __init__(self):
		super().__init__(0, 0, 0, 0, 'fusee', 'black')
	def heading(self):
		return shiphead
	def move(self):
		global speed
		global xspeed
		global yspeed
		global lost
		global ship
		global countreac
		self.y += yspeed
		self.x += xspeed
			
		xspeed = 0.99 * xspeed # histoire qu'il ne file pas à l'infini
		yspeed = 0.99 * yspeed - 0.02 # gravité

		countreac += 1
		if countreac > 20:
			ship.shape = "fusee"


def keyboard_cb(key):
	global speed
	global xspeed
	global yspeed
	global ship
	global countreac
	global shiphead
	if key == 'space' or key == 'Up':
		xspeed = xspeed + math.sin(-3.1415926535 * shiphead / 180) * 0.2
		yspeed = yspeed + math.cos(3.1415926535 * shiphead / 180) * 0.2
		
		ship.shape = "fusee reac"
		countreac = 0
	elif key == 'Escape':
		print("Au revoir...")
		engine.exit_engine()
	elif key == 'Right':
		shiphead -= 2
	elif key == 'Left':
		shiphead += 2
	else:
		print(key)


def drawfus_alt():
	global basesize
	B = basesize
	
	ship = turtle.Shape("compound")
	mesh = ((1*B,0), (2*B, 2*B), (-2*B,0), (2*B, -2*B), (1*B,0) ) 
	ship.addcomponent(mesh, "black", "black")
	
	redship = turtle.Shape("compound")
	redship.addcomponent(mesh, "red", "red")
	
	turtle.register_shape('fusee', ship)
	turtle.register_shape('fusee reac', redship)

def banner(s):
	turtle.home()
	turtle.color('black')
	turtle.write(s, True, align='center', font=('Arial', 48, 'italic'))
	time.sleep(3)
	#turtle.undo()


def drawsun():
	global sundiam
	turtle.home()
	turtle.setpos(0,-sundiam/2)
	turtle.begin_poly()
	turtle.circle(sundiam/2, None, None)
	turtle.end_poly()
	circ = turtle.get_poly()
	turtle.register_shape('sun',circ)

def drawground():
	s = turtle.Shape("compound")
	ground = ((-320, 120), (-280, 41), (-240, 27),
		(-200, 59), (-160, 25), (-120, 43), (-80, 56),
		(-40, 20), (0, 20), (40, 20), (80, 44),
		(120, 28), (160, 66), (200, 29), (240, 64),
		(280, 34), (320, 140), (320, 0), (-320,0) ) 
	s.addcomponent(ground, "#8B4513", "#8B4513")
	turtle.register_shape('ground', s)

def collision_cb_SL(sun, lander):
	if math.sqrt( (lander.x - sun.x) ** 2 + (lander.y - sun.y) ** 2 ) <= sundiam/2 + 2*basesize :
		banner("Sunned!")
		engine.exit_engine()

def collision_cb_LS(lander, sun):
    collision_cb_SL(sun, lander)

def genericGroundCollisionCall(ship, gnd):
	step = 0
	orig = 0
	for i in range(len(gnd.ground)-1):
		x0 = gnd.ground[i][0]
		y0 = gnd.ground[i][1]
		x1 = gnd.ground[i+1][0]
		y1 = gnd.ground[i+1][1]
		y = ship.y + HEIGHT /2
		x = ship.x
		if x0 <= ship.x and ship.x <= x1: # Here we are!
			a = -1 * (y1 - y0) / (x1 - x0)
			b = 1
			c = -1 * y0 + x0 * (y1 - y0) / (x1 - x0)
			d = abs(a * x + b * y + c) / math.sqrt(a ** 2 + b ** 2)
			print(math.sqrt(xspeed ** 2 + yspeed ** 2))
			if (d <= 2*basesize and a != 0) or (d <= 2*basesize and a == 0 and (abs(shiphead) >= 15 or math.sqrt(xspeed ** 2 + yspeed ** 2) >= 1 )):
				banner("Crashed!")
				engine.exit_engine()
			elif (d <= 2*basesize and a == 0 and abs(shiphead) < 15):
				banner("Landed!")
				engine.exit_engine()


def collide_SH_GD(ship, gnd):
	genericGroundCollisionCall(ship, gnd)

def collide_GD_SH(gnd, ship):
	genericGroundCollisionCall(ship, gnd)

if __name__ == '__main__':
	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine()
	engine.set_keyboard_handler(keyboard_cb)
	drawground()
	drawfus_alt()
	drawsun()

	ship = Fusee()
	gnd = Ground()
	sun = Sun()
	engine.add_obj(gnd)
	engine.add_obj(sun)	
	engine.add_obj(ship)
	# Call collision_cb_SL() each step for each pair of {Sun, Lander}
	engine.register_collision(Sun, Fusee, collision_cb_SL)
	# Call collision_cb_LS() each step for each pair of {Lander, Sun}
	engine.register_collision(Fusee, Sun, collision_cb_LS)

	engine.register_collision(Fusee, Ground, collide_SH_GD)
	engine.register_collision(Ground, Fusee, collide_GD_SH)

	engine.engine()

