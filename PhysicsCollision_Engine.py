import asyncio

import pygame
import math
import numpy as np
import time

import asyncio

pygame.init()
font = pygame.font.SysFont(None, 24)

# Open a new window
size = (1000, 750)
screen = pygame.display.set_mode(size)

sub_step = 2
frameRate = 60

dt = 2

def acc_math(pos, center, acc):
    dist = math.dist(pos, center)
    dist_vector = center - pos

    diff = dist / acc

    acc_vector = pygame.Vector2((dist_vector.x / diff)/frameRate, (dist_vector.y / diff)/frameRate)

    return acc_vector

class Engine_test:
    def __init__(self):
        pass

class VerletObject():
    def __init__(self, x, y, vx, vy, mass, r):
        self.pos = pygame.Vector2(x, y)
        self.old_pos = pygame.Vector2(x, y-1)
        self.acceleration = pygame.Vector2(vx / frameRate, vy / frameRate)

        self.friction = 0.97
        self.groundfriction = 0.7

        self.coord_in_grid = [0, 0]

        self.radius = r
        self.color = (0, 255, 0)
        self.mass = mass

    def update(self):
        vel = self.pos - self.old_pos
        self.old_pos = self.pos
        self.pos = self.pos + vel + self.acceleration * dt**2


        self.acceleration = pygame.Vector2(0, 0)

        old_adress = "{0} {1}".format(int(self.coord_in_grid[0]), int(self.coord_in_grid[1]))
        self.coord_in_grid = round(self.pos/grid_size)
        adress = "{0} {1}".format(int(self.coord_in_grid[0]), int(self.coord_in_grid[1]))

        new_data = grid[adress]
        new_data.append(self)

        new_old_data = grid[old_adress]
        if  new_old_data != []:
            new_old_data.remove(self)
            grid.update({old_adress:new_old_data})

        grid.update({adress:new_data})


    def accelerate(self, acc):
        self.acceleration += acc

    def constraint(self):
        if self.pos.x > screen.get_width() - self.radius:
            self.pos.x = screen.get_width() - self.radius

        if self.pos.x < self.radius:
            self.pos.x = self.radius

        if self.pos.y > screen.get_height() - self.radius:
            self.pos.y = screen.get_height() - self.radius

        if self.pos.y < self.radius:
            self.pos.y = self.radius

    def constraint_circle(self, radius, x, y):
        pos = (x, y)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), radius, width=1)

        toObj = self.pos - pos
        dist = math.dist(self.pos, (x, y))

        if dist > radius - self.radius:
            n = toObj / dist
            self.pos = pos + n * (radius-self.radius)

    def collision(self, obj2):
        collision_axis = self.pos - obj2.pos
        dist_2 = collision_axis.x ** 2 + collision_axis.y ** 2
        min_radius = self.radius + obj2.radius

        if (dist_2 < min_radius ** 2):
            dist = math.sqrt(dist_2)
            n = collision_axis / dist

            mass_ratio1 = self.mass / (self.mass + obj2.mass)
            mass_ratio2 = obj2.mass / (self.mass + obj2.mass)

            delta = 0.5 * 0.75 * (dist - min_radius)

            self.pos -= n * (mass_ratio2 * delta)
            obj2.pos += n * (mass_ratio1 * delta)
            return True

    def draw(self):
        pygame.draw.circle(screen, (0, 255, 255), self.pos, self.radius)

dot1 = VerletObject(700, 200, 1, 1, 1, 4)
dot2 = VerletObject(800, 200, 1, 1, 1, 4)

dots = []
grid = {}
grid_size = 10
grid_stepX = size[0]/grid_size
grid_stepY = size[1]/grid_size

for y in range(0, int(grid_stepY)):
    for x in range(0, int(grid_stepX)):
        grid.update({"{0} {1}".format(x, y):[]})

dots.append(dot1)
dots.append(dot2)

exit = False

gravity = pygame.Vector2(0/frameRate, 1/frameRate)

Engine = Engine_test()

Collision = False

if len(dots) > 1:
    collision = True

dotsNumber = 300
spawnRate = 1
spawnTimer = 1

check = []

clock = pygame.time.Clock()

while not exit:
    screen.fill((0, 0, 0))

    pygame.draw.circle(screen, (255, 0, 0), (500, 500), 1)

    if spawnTimer == 0 and dotsNumber != 0:
        dots.append(VerletObject(500, 400, 1, 1, 1, 4))
        dotsNumber -= 1
        spawnTimer = spawnRate

    for x in dots:
        x.accelerate(acc_math(x.pos, pygame.Vector2(500, 500), 2))
        #acc_math(x.pos, pygame.Vector2(500, 500), 2)
        x.update()
        x.constraint_circle(300, 500, 400)

        for step in range(0, sub_step):
            grid_obj = (int(x.coord_in_grid[0]), int(x.coord_in_grid[1]))

            for ty in range(0, 3):
                for tx in range(0, 3):
                    objects = grid["{0} {1}".format((grid_obj[0] - (tx - 1)), grid_obj[1] - (ty - 1))]
                    if len(objects) > 0:
                        for test in objects:
                            if test != x:
                                x.collision(test)

    for x in dots:
        x.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dots.append(VerletObject(500, 200, 1, 1, 10, 10))

    text1 = font.render("number of objects {0}".format(len(dots)), True, (0, 255, 0))
    screen.blit(text1, (0, 50))

    pygame.display.set_caption(str(clock.get_fps()))
    spawnTimer -= 1
    pygame.display.update()
    time.sleep(1/frameRate)

    clock.tick(60)