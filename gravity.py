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

### GLOBALS ###

countreac = 0 # compteur de frames du réacteur
basesize = 10 # unité de base du vaisseau
sundiam = 150 # diamètre du soleil
wlength = 5000 # sol

rocket_power = 0.3 # pêche des moteurs
gravity_coef = 0.03 # attraction lunaire
slowdown = 0.99 # frottement
fuel_consumption = 0.2  # consommation d'essence

lvl = () # le level est généré aléatoirement

class GreenBarFuel(engine.GameObject):
	def __init__(self):
		super().__init__(-300, 130, 0, 0, 'essence', 'green')
	def heading(self):
		return 180

class SpeedBar(engine.GameObject):
	def __init__(self):
		super().__init__(300, 130, 0, 0, 'speed', 'red')
	def heading(self):
		return 180

class LogoEssence(engine.GameObject):
	def __init__(self):
		super().__init__(-280, 160, 0, 0, 'ess.gif', 'green')

class LogoVitesse(engine.GameObject):
	def __init__(self):
		super().__init__(270, 160, 0, 0, 'speed.gif', 'green')

class Enemy(engine.GameObject):
	def __init__(self):
		super().__init__(0,0,0,0,'enemy','red')

class Ground(engine.GameObject):
	def __init__(self):
		super().__init__(0, -HEIGHT/2, 0, 0, 'ground', '#8B4513')
	def heading(self):
		return 90
	def isoob(self):
		return False
	#ground = lvl
	ground = ()
	gndIdentifier = 0
	

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
		global gnd
		
		if self.mode == 1 and self.fuelLevel > 0:
			ship.xspeed += math.sin(-3.1415926535 * ship.head / 180) \
			* rocket_power * self.gazpower
			ship.yspeed += math.cos(3.1415926535 * ship.head / 180)  \
			* rocket_power * self.gazpower

		# If the ship is in the last third of the screen (whichever side it is),
		# then scroll the ground!
		if abs(self.x) <= (1/3) * WIDTH:
			self.y += self.yspeed
			self.x += self.xspeed
		else:
			gnd.x -= self.xspeed

			if gnd.x >= -1 * WIDTH / 2 or gnd.x <= -wlength + WIDTH / 2:
				# print(gnd.x)
				if gnd.x >= -1 * WIDTH / 2:
					if gnd.gndIdentifier == 1:
						gndbis.x = gnd.x - wlength
					else:
						gndpr.x = gnd.x - wlength
				else:
					if gnd.gndIdentifier == 1:
						gndbis.x = gnd.x + wlength
					else:
						gndpr.x = gnd.x + wlength
				if gnd.x >= 0 or gnd.x <= -wlength:
					if gnd.gndIdentifier == 1:
						gnd = gndbis
					else:
						gnd = gndpr		
			self.y += self.yspeed
			
		self.xspeed = slowdown * self.xspeed
		self.yspeed = slowdown * self.yspeed - gravity_coef

		
		if self.mode == 0:
			self.shape = "fusee"
		
		if self.fuelLevel > 0 and self.mode == 1:
			self.fuelLevel -= fuel_consumption * self.gazpower
			drawFuelBar(self.fuelLevel)
			ess.shape = "essence"
			if self.fuelLevel <= 0:
				self.gazpower = 0
				self.shape = "fusee"
				self.mode = 0
		
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
	gazpower = 0 # increased at each press on q, decreased at each press on s



def keyboard_cb(key):
	# Problem on some machines: if a key stays pressed, then
	# there is a delay between the first key event being triggered
	# and the next ones (this is the damn repeat delay)
	# How to get around this issue?
	global ship
	global countreac
	if key == 'q' and ship.fuelLevel > 0:
		ship.mode = 1
		ship.gazpower += 0.05
		drawSpeedBar(100 * ship.gazpower)
		spd.shape = "speed"
		ship.shape = "fusee reac"
	elif key == 's':
		ship.gazpower -= 0.05
		drawSpeedBar(100 * ship.gazpower)
		spd.shape = "speed"
		if ship.gazpower <= 0:
			ship.gazpower = 0
			ship.mode = 0
			ship.shape = "fusee"
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
	ship.addcomponent(mesh, "#555555", "#555555")
	
	redship = turtle.Shape("compound")
	reaction = ((1.5*B, 1*B), (2*B, 0), (1.5*B, -1*B), (1*B, 0))
	
	redship.addcomponent(mesh, "#555555", "#555555")
	redship.addcomponent(reaction, "yellow", "yellow") # réacteur, (c) Antonin
	
	turtle.register_shape('fusee', ship)
	turtle.register_shape('fusee reac', redship)

def banner(s):
	turtle.home()
	turtle.color('white')
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

def drawFuelBar(flevel):
	s = turtle.Shape("compound")
	rect = ((flevel, 0), (flevel, 10), (0,10), (0,0))
	s.addcomponent(rect, "#008000", "#008000")
	turtle.register_shape('essence',s)

def drawSpeedBar(level):
	s = turtle.Shape("compound")
	rect = ((level, 0), (level, 10), (0,10), (0,0))
	s.addcomponent(rect, "#FF3000", "#FF3000")
	turtle.register_shape('speed',s)


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
		if x0 <= x and x <= x1 and x1 != x0 and y - 2 * basesize < max(y1, y0):
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
			elif (d <= 2*basesize and abs(a) <= 1 and math.sqrt(ship.xspeed ** 2 + \
				ship.yspeed ** 2) >= 1 ):
				banner("Fast crash...")
				engine.exit_engine()
			elif (d <= 2*basesize and abs(a) <= 1 and abs(ship.head) < 15):
				banner("Landed!")
				engine.exit_engine()


def collide_SH_GD(ship, gnd):
	genericGroundCollisionCall(ship, gnd)

def collide_GD_SH(gnd, ship):
	genericGroundCollisionCall(ship, gnd)

def recursiveFractalBuild(x0, x1, y0, y1, w, rr):
	if w == 0:
		return [( (x0 + x1) / 2., (y0 + y1) / 2. + random.randint(0,rr))]
	else:
		ymid = (y0 + y1) / 2 + random.randint(0,rr)
		LG = recursiveFractalBuild(x0, (x0 + x1) /2., y0, ymid, w-1, int(rr / 1.5))
		LD = recursiveFractalBuild((x0 + x1) /2., x1, ymid, y1, w-1, int(rr / 1.5))
		L = []
		for i in LG:
			L.append(i)
		L.append(( (x0 + x1) / 2., ymid ))
		for i in LD:
			L.append(i)
		return L

def build_random_map(width):
	zero_pos = random.randint(0, width-100) # Where to put the flat spot.
	
	n = 6 # divide the total width in n equal parts
	depth = 5 # recursion depth for fractal calculation
	interv = 90 # maximal amplitude, divided by 2 at each recursion round

	mountains = []
	yprev = random.randint(20,120)
	ydeb = yprev

	for i in range(n):
		y0 = random.randint(20,120)
		#y1 = random.randint(20,120)
		mnt = recursiveFractalBuild(int(i * width / n), int((i + 1) * width / n), \
		yprev, y0, depth, interv)
		
		mnt.append((int(i * width / n), yprev))
		mnt.append((int((i + 1) * width / n), y0))
		yprev = y0
		for j in mnt:
			mountains.append(j)

	mountains[len(mountains)-1] = (width, ydeb) # continuity for scrolling

	#mountains = recursiveFractalBuild(0, width, y0, y1, 7, 120)
	#mountains.append((0, y0))
	#mountains.append((width, y1))
	mnt_sort = sorted(mountains, key=lambda x: x[0])
	
	# find the closest spot
	closest_point = mnt_sort[0]
	closest_dist = width
	for i in mnt_sort:
		if abs(i[0] - zero_pos) <= closest_dist:
			closest_point = i
			closest_dist = abs(i[0] - zero_pos)
	
	ret = [ x if x[0] > zero_pos + 100 or x[0] < zero_pos \
	 else (x[0], closest_point[1]) for x in mnt_sort ] # just like a bulldozer!!
	ret.append((width, 0))
	ret.append((0, 0))
	#mnt_sort.append((width, 0))
	#mnt_sort.append((0,0))
	
	return tuple(ret)
	#return tuple(mnt_sort)


if __name__ == '__main__':
	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine()
	engine.set_keyboard_handler(keyboard_cb)
	lvl = build_random_map(wlength)
	turtle.bgcolor("#000044")
	drawground()
	drawfus_alt()
	drawsun()
	drawFuelBar(100)
	drawSpeedBar(0)
	turtle.register_shape("ess.gif")
	turtle.register_shape("speed.gif")

	ship = Fusee()
	gndpr = Ground()
	gndpr.gndIdentifier = 1
	gndpr.ground = lvl
	gndpr.x = -wlength / 2
	
	gndbis = Ground()
	gndbis.gndIdentifier = 2
	gndbis.ground = lvl
	gndbis.x = wlength / 2
	
	gnd = gndpr

	sun = Sun()
	ess = GreenBarFuel()
	spd = SpeedBar()
	engine.add_obj(gndpr)
	engine.add_obj(gndbis)
	engine.add_obj(sun)

	engine.add_obj(ess)
	engine.add_obj(spd)
	
	logo = LogoEssence()
	vits = LogoVitesse()
	engine.add_obj(logo)
	
	engine.add_obj(ship)
	
	engine.register_collision(Sun, Fusee, collision_cb_SL)
	engine.register_collision(Fusee, Sun, collision_cb_LS)

	engine.register_collision(Fusee, Ground, collide_SH_GD)
	engine.register_collision(Ground, Fusee, collide_GD_SH)
	
	
	engine.engine()

