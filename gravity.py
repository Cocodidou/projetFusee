#!/usr/bin/env python3
# coding: UTF-8
# ship landing game

import turtle
import engine
import random
import math
import time
import os

WIDTH = 1024
HEIGHT = 768

# GLOBALS #

basesize = 10  # base ship unit
sundiam = 150  # sun diameter
wlength = 5000  # ground length

rocket_power = 1  # how much acceleration should the rockets give the ship
gravity_coef = 0.06
slowdown = 0.99
fuel_consumption = 0.1

lvl = ()  # level is randomly generated, but is still global (dirty!)


class GreenBarFuel(engine.GameObject):
    def __init__(self):
        super().__init__(-WIDTH/2+20, 130, 0, 0, 'fuel', 'green')

    def heading(self):
        return 180


class SpeedBar(engine.GameObject):
    def __init__(self):
        super().__init__(WIDTH/2-20, 130, 0, 0, 'speed', 'red')

    def heading(self):
        return 180


class FuelLogo(engine.GameObject):
    def __init__(self):
        super().__init__(-WIDTH/2+40, 160, 0, 0, 'ess.gif', 'green')


class AccelerationLogo(engine.GameObject):
    def __init__(self):
        super().__init__(WIDTH/2-50, 160, 0, 0, 'speed.gif', 'green')


class Enemy(engine.GameObject):
    def __init__(self):
        super().__init__(0, 0, 0, 0, 'enemy', 'red')

    def heading(self):
        return self.head

    def isoob(self):
        return False  # enemies should never be destroyed by oob

    def move(self):
        self.y0 += self.yspeed
        self.x0 += self.xspeed

        self.x = (gnd.x + wlength/2) + self.x0
        self.y = self.y0

        # All the enemies have to converge towards the player
        re = math.sqrt((self.y - ship.y) ** 2 + (self.x - ship.x) ** 2)
        self.head = 180 / 3.1415926535 * 2 * \
            math.atan((self.y - ship.y) / ((self.x - ship.x) + re)) + 90

        self.xspeed = math.sin(-3.1415926535 * (self.head - 90) / 180) \
            * rocket_power
        self.yspeed = math.cos(3.1415926535 * (self.head - 90) / 180)  \
            * rocket_power

        if random.randint(0, 1000) >= 992:
            shoot(self)

    xspeed = 0
    yspeed = 0
    x0 = 0
    y0 = 0
    head = 90


class Bullet(engine.GameObject):
    def __init__(self, xs, ys, x, y, hd):
        self.xspeed = xs
        self.yspeed = ys
        self.head = hd
        super().__init__(x, y, 0, 0, 'bullet', 'red')

    def heading(self):
        return self.head

    def move(self):
        self.x += self.xspeed
        self.y += self.yspeed

    head = 0
    xspeed = 0
    yspeed = 0


class Ground(engine.GameObject):
    def __init__(self):
        super().__init__(0, -HEIGHT/2, 0, 0, 'ground', '#8B4513')

    def heading(self):
        return 90

    def isoob(self):
        return False

    ground = ()  # this will be defined as lvl

    # There are two grounds, which are alternatively used
    # while scrolling. This variable helps distinguishing them.
    gndIdentifier = 0


class Sun(engine.GameObject):
    def __init__(self):
        super().__init__(0, HEIGHT/2, 0, 0, 'sun', 'yellow')


class Fusee(engine.GameObject):
    def __init__(self):
        super().__init__(0, 0, 0, 0, 'lander', 'black')

    def heading(self):
        return self.head

    def move(self):
        global gnd

        if self.mode == 1 and self.fuel_level > 0:
            self.xspeed += math.sin(-3.1415926535 * self.head / 180) \
                * rocket_power * self.acceleration
            self.yspeed += math.cos(3.1415926535 * self.head / 180)  \
                * rocket_power * self.acceleration

        if abs(self.x) <= (1/6) * WIDTH \
            or (self.x >= (1/6) * WIDTH and self.xspeed < 0) \
                or (self.x <= -(1/6) * WIDTH and self.xspeed > 0):
            self.y += self.yspeed
            self.x += self.xspeed
        else:
            gnd.x -= self.xspeed  # scroll the ground instead of the ship
            if gnd.x >= -1 * WIDTH / 2 or gnd.x <= -wlength + WIDTH / 2:
                # we are in a sensitive zone; two grounds are being shown
                if gnd.x >= -1 * WIDTH / 2:
                    if gnd.gndIdentifier == 1:
                        sec_ground.x = gnd.x - wlength
                    else:
                        pri_ground.x = gnd.x - wlength
                else:
                    if gnd.gndIdentifier == 1:
                        sec_ground.x = gnd.x + wlength
                    else:
                        pri_ground.x = gnd.x + wlength
                if gnd.x >= 0 or gnd.x <= -wlength:
                    # it's now time to switch the primary ground
                    # (reference for x's)
                    if gnd.gndIdentifier == 1:
                        gnd = sec_ground
                    else:
                        gnd = pri_ground
            self.y += self.yspeed

        self.xspeed = slowdown * self.xspeed
        self.yspeed = slowdown * self.yspeed - gravity_coef

        if self.mode == 0:  # in case it hasn't got done before...
            self.shape = "lander"

        if self.fuel_level > 0 and self.mode == 1:
            self.fuel_level -= fuel_consumption * self.acceleration
            reg_fuel_bar(self.fuel_level)
            ess.shape = "fuel"
            if self.fuel_level <= 0:
                self.acceleration = 0
                self.shape = "lander"
                self.mode = 0

    def isoob(self):
        return False  # the ship shouldn't get destroyed

    def getFuelLevel(self):
        return fuel_level

    xspeed = 0
    yspeed = 0
    fuel_level = 100
    head = 0
    mode = 0
    acceleration = 0


# Shoots a bullet from the sender, with its heading and speed plus a constant.
def shoot(sender):
    bh = sender.heading()
    abs_spd = math.sqrt(sender.xspeed ** 2 + sender.yspeed ** 2) + 8
    bxs = abs_spd * math.sin(-3.1415926535 * bh / 180)
    bys = abs_spd * math.cos(-3.1415926535 * bh / 180)
    bx = sender.x + 4 * basesize * \
        math.sin(-3.1415926535 * sender.heading() / 180)
    by = sender.y + 4 * \
        basesize * math.cos(-3.1415926535 * sender.heading() / 180)
    bullet = Bullet(bxs, bys, bx, by, bh)
    engine.add_obj(bullet)


# Handle keyboard events.
def keyboard_cb(key):
    global ship  # assuming it's unique (and this is the case!)
    global spd  # the accelerometer
    if key == 'q' and ship.fuel_level > 0:
        ship.mode = 1
        ship.acceleration += 0.05
        reg_speed_bar(100 * ship.acceleration)
        spd.shape = "speed"
        ship.shape = "powered_lander"
    elif key == 's':
        ship.acceleration -= 0.05
        reg_speed_bar(100 * ship.acceleration)
        spd.shape = "speed"
        if ship.acceleration <= 0:
            ship.acceleration = 0
            ship.mode = 0
            ship.shape = "lander"
    elif key == 'Escape':
        engine.exit_engine()
    elif key == 'Right':
        ship.head -= 8
    elif key == 'Left':
        ship.head += 8
    elif key == "space":
        shoot(ship)

# Graphical functions.


# Displays a message on screen.
def banner(s):
    turtle.home()
    turtle.color('white')
    turtle.write(s, True, align='center', font=('Monospace', 48, 'italic'))
    time.sleep(3)


# Registers the ship.
def reg_ship():
    global basesize
    B = basesize

    ship = turtle.Shape("compound")
    mesh = ((1*B, 0), (2*B, 2*B), (-2*B, 0), (2*B, -2*B), (1*B, 0))
    ship.addcomponent(mesh, "#555555", "#555555")

    redship = turtle.Shape("compound")
    reaction = ((1.5*B, 1*B), (2*B, 0), (1.5*B, -1*B), (1*B, 0))

    redship.addcomponent(mesh, "#555555", "#555555")
    redship.addcomponent(reaction, "yellow", "yellow")

    turtle.register_shape('lander', ship)
    turtle.register_shape('powered_lander', redship)


# Registers the enemy.
def reg_enemy():
    global basesize
    B = 2*basesize
    enemyship = turtle.Shape("compound")
    enemy_mesh = ((0, -1*B), (1*B, -0.33*B), (1*B, 0.33*B),
                  (0, 1*B), (-1*B, 0))
    left_antenna = ((-0.33*B, -0.66*B), (-B, -B), (-0.66*B, -0.33*B))
    right_antenna = ((-0.33*B, 0.66*B), (-B, B), (-0.66*B, 0.33*B))

    enemyship.addcomponent(enemy_mesh, "red", "green")
    enemyship.addcomponent(left_antenna, "red", "green")
    enemyship.addcomponent(right_antenna, "red", "green")
    turtle.register_shape("enemy", enemyship)


# Registers the bullet.
def reg_bullet():
    turtle.home()
    turtle.setpos(0, -5)
    turtle.begin_poly()
    turtle.circle(5, None, None)
    turtle.end_poly()
    circ = turtle.get_poly()
    turtle.register_shape('bullet', circ)


# Registers the sun.
def reg_sun():
    global sundiam
    turtle.home()
    turtle.setpos(0, -sundiam / 2)
    turtle.begin_poly()
    turtle.circle(sundiam/2, None, None)
    turtle.end_poly()
    circ = turtle.get_poly()
    turtle.register_shape('sun', circ)


# Registers the ground, once created.
def reg_ground():
    s = turtle.Shape("compound")
    s.addcomponent(lvl, "#8B4513", "#8B4513")
    turtle.register_shape('ground', s)


# Registers the fuel bar, with the given fuel level.
def reg_fuel_bar(flevel):
    s = turtle.Shape("compound")
    rect = ((flevel, 0), (flevel, 10), (0, 10), (0, 0))
    s.addcomponent(rect, "#008000", "#008000")
    turtle.register_shape('fuel', s)


# Registers the acelerometer bar, with the given acceleration.
def reg_speed_bar(level):
    s = turtle.Shape("compound")
    rect = ((level, 0), (level, 10), (0, 10), (0, 0))
    s.addcomponent(rect, "#FF3000", "#FF3000")
    turtle.register_shape('speed', s)


# Handle collisions between the ship and the sun
def collision_cb_SL(sun, lander):
    if math.sqrt((lander.x - sun.x) ** 2 + (lander.y - sun.y) ** 2) \
            <= sundiam/2 + 2 * basesize:
        banner("Sunned!")
        engine.exit_engine()


def collision_cb_LS(lander, sun):
    collision_cb_SL(sun, lander)


# Handle collisions between the ship and enemies
def collision_enemy(en, lander):
    if math.sqrt((lander.x - en.x) ** 2 + (lander.y - en.y) ** 2) \
            <= 4 * basesize:
        banner("Crash against enemy")
        engine.exit_engine()


# Handle collisions between ennemies and bullets
def collision_en_bl(en, bl):
    if math.sqrt((bl.x - en.x) ** 2 + (bl.y - en.y) ** 2) <= 4 * basesize:
        engine.del_obj(en)
        engine.del_obj(bl)


def collision_bl_en(bl, en):
    collision_en_bl(en, bl)


# Handle collisions between the ship and bullets
def collision_sh_bl(lander, bl):
    if math.sqrt((bl.x - lander.x) ** 2 + (lander.y - bl.y) ** 2) \
            <= 2 * basesize:
        banner("Killed by bullet")
        engine.exit_engine()


def collision_bl_sh(bl, lander):
    collision_sh_bl(lander, bl)


# Handle collisions between thhe ship and the ground
def collision_ship_ground(lander, terrain):
    step = 0
    orig = 0
    y = lander.y + HEIGHT / 2
    x = lander.x - terrain.x
    for i in range(len(terrain.ground)-1):
        x0 = terrain.ground[i][0]
        y0 = terrain.ground[i][1]
        x1 = terrain.ground[i+1][0]
        y1 = terrain.ground[i+1][1]
        if x0 <= x and x <= x1 and x1 != x0 and y - 2 * basesize < max(y1, y0):
            # BAD HACK: there should be no test on y
            a = y0 - y1
            b = x1 - x0
            c = (x0 - x1) * y0 + (y1 - y0) * x0
            d = abs(a * x + b * y + c) / math.sqrt(a ** 2 + b ** 2)
            if (d <= basesize and a != 0):
                banner("Crash!")
                engine.exit_engine()
            elif (d <= 2*basesize and abs(a) <= 1 and abs(lander.head) >= 15):
                banner("Crash on one reactor!")
                engine.exit_engine()
            elif (d <= 2*basesize and abs(a) <= 1 and
                    math.sqrt(lander.xspeed ** 2 + lander.yspeed ** 2) >= 2):
                banner("Fast crash...")
                engine.exit_engine()
            elif (d <= 2*basesize and abs(a) <= 1 and abs(lander.head) < 15):
                banner("Landed!")
                engine.exit_engine()


def collision_ground_ship(gnd, ship):
    collision_ship_ground(ship, gnd)


# Fractal creation of the ground
def recursiveFractalBuild(x0, x1, y0, y1, w, rr):
    if w == 0:
        return [((x0 + x1) / 2., (y0 + y1) / 2. + random.randint(0, rr))]
    else:
        ymid = (y0 + y1) / 2 + random.randint(0, rr)
        LL = recursiveFractalBuild(x0, (x0 + x1) / 2., y0, ymid,
                                   w-1, int(rr / 1.5))
        RL = recursiveFractalBuild((x0 + x1) / 2., x1, ymid, y1,
                                   w-1, int(rr / 1.5))
        L = []
        for i in LL:
            L.append(i)
        L.append(((x0 + x1) / 2., ymid))
        for i in RL:
            L.append(i)
        return L


# Creates a random terrain with a flat spot (the one to land on)
def build_random_map(width):
    zero_pos = random.randint(0, width-100)  # Where to put the flat spot.

    n = 6  # divide the total width in n equal parts
    depth = 5  # recursion depth for fractal calculation
    interv = 90  # maximal amplitude, divided by 2 at each recursion round

    mountains = []
    yprev = random.randint(20, 120)
    ydeb = yprev  # continuity index for scrolling

    # the ground is created by applying the fractal procedure to n equal parts
    for i in range(n):
        y0 = random.randint(20, 120)
        mnt = recursiveFractalBuild(int(i * width / n),
                                    int((i + 1) * width / n),
                                    yprev, y0, depth, interv)

        mnt.append((int(i * width / n), yprev))
        mnt.append((int((i + 1) * width / n), y0))
        yprev = y0
        for j in mnt:
            mountains.append(j)

    mountains[len(mountains)-1] = (width, ydeb)
    mnt_sort = sorted(mountains, key=lambda x: x[0])

    # find the closest spot
    closest_point = mnt_sort[0]
    closest_dist = width
    for i in mnt_sort:
        if abs(i[0] - zero_pos) <= closest_dist:
            closest_point = i
            closest_dist = abs(i[0] - zero_pos)

    ret = [x if x[0] > zero_pos + 100 or x[0] < zero_pos
           else (x[0], closest_point[1]) for x in mnt_sort]
    # make the flat spot just like a bulldozer would do!!

    ret.append((width, 0))
    ret.append((0, 0))

    return tuple(ret)


if __name__ == '__main__':
    engine.init_screen(WIDTH, HEIGHT)
    engine.init_engine()
    engine.set_keyboard_handler(keyboard_cb)

    # build the level
    lvl = build_random_map(wlength)

    # we're on the moon...
    turtle.bgcolor("#000044")

    # register the shapes
    reg_ground()
    reg_ship()
    reg_sun()
    reg_enemy()
    reg_bullet()
    reg_fuel_bar(100)
    reg_speed_bar(0)

    # register the gifs
    turtle.register_shape("ess.gif")
    turtle.register_shape("speed.gif")

    # create the objects

    ship = Fusee()

    # primary ground
    pri_ground = Ground()
    pri_ground.gndIdentifier = 1
    pri_ground.ground = lvl
    pri_ground.x = -wlength / 2

    # secondary ground
    sec_ground = Ground()
    sec_ground.gndIdentifier = 2
    sec_ground.ground = lvl
    sec_ground.x = wlength / 2

    # for now, the ground is assumed to be the primary
    gnd = pri_ground

    sol = Sun()

    # these are level bars
    ess = GreenBarFuel()
    spd = SpeedBar()

    engine.add_obj(pri_ground)
    engine.add_obj(sec_ground)
    engine.add_obj(sol)
    engine.add_obj(ess)
    engine.add_obj(spd)

    # display the gifs on screen
    logo = FuelLogo()
    accl = AccelerationLogo()
    engine.add_obj(logo)
    engine.add_obj(accl)

    engine.add_obj(ship)

    # create a random number of enemies located at random places
    nb_enemies = random.randint(5, 10)
    for i in range(nb_enemies):
        en = Enemy()
        en.x0 = random.randint(-wlength/2, wlength/2)
        en.y0 = random.randint(-HEIGHT/2, HEIGHT/2)
        engine.add_obj(en)

    # register collisions
    engine.register_collision(Sun, Fusee, collision_cb_SL)
    engine.register_collision(Fusee, Sun, collision_cb_LS)

    engine.register_collision(Fusee, Ground, collision_ship_ground)
    engine.register_collision(Ground, Fusee, collision_ground_ship)

    engine.register_collision(Fusee, Enemy, collision_enemy)

    engine.register_collision(Enemy, Bullet, collision_en_bl)
    engine.register_collision(Fusee, Bullet, collision_sh_bl)
    engine.register_collision(Bullet, Fusee, collision_bl_sh)

    # start the game!
    engine.engine()
