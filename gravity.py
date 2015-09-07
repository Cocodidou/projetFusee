#!/usr/bin/env python3
# coding: UTF-8
# basic moving ship

import turtle
import engine
import random
import math
import time
import os

WIDTH = 640
HEIGHT = 480

countreac = 0 # compteur de frames du réacteur
basesize = 10 # unité de base du vaisseau
sundiam = 150 # diamètre du soleil
wlength = 5000 # sol

lvl = () # le level est généré aléatoirement

class Ground(engine.GameObject):
	def __init__(self):
		super().__init__(0, -HEIGHT/2, 0, 0, 'ground', '#8B4513')
	def heading(self):
		return 90
	def isoob(self):
		return False
	#ground = lvl
	ground = ()
	

class Sun(engine.GameObject):
	def __init__(self):
		super().__init__(0, HEIGHT/2, 0, 0, 'sun', 'yellow')
		#super().__init__(0, 0, 0, 0, 'sun', 'yellow')

class Fusee(engine.GameObject):
	def __init__(self):
		super().__init__(0, 0, 0, 0, 'fusee', 'black')
	def heading(self):
		return self.head
	def move(self):
		global ship
		global countreac
		
		if abs(self.x) <= (1/3) * WIDTH \
		or (self.x >= (1/3) * WIDTH and self.xspeed < 0) \
		or (self.x <= -(1/3) * WIDTH and self.xspeed > 0) \
		or (gnd.x >= -1 * WIDTH / 2 and self.x <= (1/3) * WIDTH) \
		or (gnd.x <= WIDTH/2 - wlength and self.x >= -1 * (1/3) * WIDTH):
			self.y += self.yspeed
			self.x += self.xspeed
		else:
			gnd.x -= self.xspeed
			self.y += self.yspeed
			
		self.xspeed = 0.99 * self.xspeed # histoire qu'il ne file pas à l'infini
		self.yspeed = 0.99 * self.yspeed - 0.02 # gravité

		
		if countreac <= 20:
			if countreac < 20:
				countreac += 1 
			else:
				self.shape = "fusee"
				self.mode = 0
		
		if self.fuelLevel > 0 and self.mode == 1:
			self.fuelLevel -= 0.05
			drawBar(self.fuelLevel)
			ess.shape = "essence"
		
	def isoob(self):
		if super().isoob():
			if self.x <= -WIDTH/2:
				self.x = WIDTH / 2
			elif self.x >= WIDTH/2:
				self.x = -WIDTH / 2
		return False
	
	def getFuelLevel(self):
		return fuelLevel
	
	xspeed = 0
	yspeed = 0
	fuelLevel = 100
	head = 0
	mode = 0

class GreenBarFuel(engine.GameObject):
	def __init__(self):
		super().__init__(-300, 130, 0, 0, 'essence', 'green')
	def heading(self):
		return 180

class LogoEssence(engine.GameObject):
	def __init__(self):
		super().__init__(-280, 160, 0, 0, 'ess.gif', 'green')

class Enemy(engine.GameObject):
	def __init__(self):
		super().__init__(0,0,0,0,'enemy','red')

def keyboard_cb(key):
	# Problem on some machines: if a key stays pressed, then
	# there is a delay between the first key event being triggered
	# and the next ones (this is the damn repeat delay)
	# How to get around this issue?
	global ship
	global countreac
	if key == 'space' or key == 'Up':
		if ship.fuelLevel > 0:
			ship.mode = 1
			ship.xspeed +=  math.sin(-3.1415926535 * ship.head / 180) * 0.2
			ship.yspeed += math.cos(3.1415926535 * ship.head / 180) * 0.2
			ship.shape = "fusee reac"
			countreac = 0
	elif key == 'Escape':
		#print("Au revoir...")
		engine.exit_engine()
	elif key == 'Right':
		ship.head -= 2
	elif key == 'Left':
		ship.head += 2

def drawfus_alt():
	global basesize
	B = basesize
	
	ship = turtle.Shape("compound")
	mesh = ((1*B,0), (2*B, 2*B), (-2*B,0), (2*B, -2*B), (1*B,0) ) 
	ship.addcomponent(mesh, "black", "black")
	
	redship = turtle.Shape("compound")
	reaction = ((1.5*B, 1*B), (2*B, 0), (1.5*B, -1*B), (1*B, 0))
	
	redship.addcomponent(mesh, "black", "black")
	redship.addcomponent(reaction, "red", "red") # réacteur, (c) Antonin
	
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
	s.addcomponent(lvl, "#8B4513", "#8B4513")
	turtle.register_shape('ground', s)

def drawBar(flevel):
	s = turtle.Shape("compound")
	rect = ((flevel, 0), (flevel, 10), (0,10), (0,0))
	s.addcomponent(rect, "#008000", "#008000")
	turtle.register_shape('essence',s)

def collision_cb_SL(sun, lander):
	if math.sqrt( (lander.x - sun.x) ** 2 + (lander.y - sun.y) ** 2 ) <= sundiam/2 + 2*basesize :
		banner("Sunned!")
		engine.exit_engine()

def collision_cb_LS(lander, sun):
    collision_cb_SL(sun, lander)

def genericGroundCollisionCall(ship, gnd):
	step = 0
	orig = 0
	y = ship.y + HEIGHT /2
	x = ship.x - gnd.x
	for i in range(len(gnd.ground)-1):
		x0 = gnd.ground[i][0]
		y0 = gnd.ground[i][1]
		x1 = gnd.ground[i+1][0]
		y1 = gnd.ground[i+1][1]
		if x0 < x and x < x1 and x1 != x0 and y - 2 * basesize < max(y1, y0):
			# BAD HACK: le test sur y ne doit pas être nécessaire
			# mathématiquement parlant
			a = y0 - y1
			b = x1 - x0
			c = (x0 - x1) * y0 + (y1 - y0) * x0
			d = abs(a * x + b * y + c) / math.sqrt(a ** 2 + b ** 2)
			#print(d)
			if (d <= basesize and a != 0):
				#print(str(x0) + ":" + str(y0) + ";" + str(x1) + ":" + str(y1))
				banner("Crashed!")
				engine.exit_engine()
			elif (d <= 2*basesize and abs(a) <= 1 and abs(ship.head) >= 15):
				banner("Crash on one reactor!")
				engine.exit_engine()
			elif (d <= 2*basesize and abs(a) <= 1 and math.sqrt(ship.xspeed ** 2 + ship.yspeed ** 2) >= 1 ):
				banner("Fast crash...")
				engine.exit_engine()
			elif (d <= 2*basesize and abs(a) <= 1 and abs(ship.head) < 15):
				banner("Landed!")
				engine.exit_engine()


def collide_SH_GD(ship, gnd):
	genericGroundCollisionCall(ship, gnd)

def collide_GD_SH(gnd, ship):
	genericGroundCollisionCall(ship, gnd)

def recursiveFractalBuild(x0, x1, w):
	if w == 0:
		return [( (x0 + x1) / 2., random.randint(20,120))]
	else:
		LG = recursiveFractalBuild(x0, (x0 + x1) /2., w-1)
		LD = recursiveFractalBuild((x0 + x1) /2., x1, w-1)
		L = []
		for i in LG:
			L.append(i)
		L.append(( (x0 + x1) / 2., random.randint(20,120)))
		for i in LD:
			L.append(i)
		return L

def build_random_map(width):
	#random.seed(os.time())
	zero_pos = random.randint(0, width-100)
	
	#num_mountains = random.randint(50, 70)
	
	#mountains = []
	
	#mountains.append((0, random.randint(20,120)))
	#mountains.append((width, random.randint(20,120)))
	
	#mountains.append((zero_pos, 20))
	#mountains.append((zero_pos + 100, 20))
	
	#ins = 0
	
	# La technique la plus pourrie du monde pour séparer des montagnes
	# en attendant de faire ça "fractalement"
	
	#while ins < num_mountains:
		#t = (random.randint(20,  width - 20), random.randint(20,120))
		#prob = False
		#for j in mountains:
			#if abs(t[0] - j[0]) <= 50:
				#prob = True
		#if prob == False:
			#ins += 1
			#mountains.append(t)
		##print(ins)
		
	mountains = recursiveFractalBuild(0, width, 6)
	mnt_sort = sorted(mountains, key=lambda x: x[0])
	
	ret = [ x if x[0] > zero_pos + 100 or x[0] < zero_pos else (x[0], 20) for x in mnt_sort ]
	ret.append((width, 0))
	ret.append((0, 0))
	
	return tuple(ret)


if __name__ == '__main__':
	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine()
	engine.set_keyboard_handler(keyboard_cb)
	lvl = build_random_map(wlength)
	drawground()
	drawfus_alt()
	drawsun()
	drawBar(100)
	turtle.register_shape("ess.gif")

	ship = Fusee()
	gnd = Ground()
	gnd.ground = lvl
	gnd.x = -wlength / 2
	sun = Sun()
	ess = GreenBarFuel()
	engine.add_obj(gnd)
	engine.add_obj(sun)	

	engine.add_obj(ess)
	
	logo = LogoEssence()
	engine.add_obj(logo)
	
	engine.add_obj(ship)
	
	engine.register_collision(Sun, Fusee, collision_cb_SL)
	engine.register_collision(Fusee, Sun, collision_cb_LS)

	engine.register_collision(Fusee, Ground, collide_SH_GD)
	engine.register_collision(Ground, Fusee, collide_GD_SH)

	engine.engine()

