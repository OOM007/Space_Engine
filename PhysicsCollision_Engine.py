import pygame
import math
import numpy as np
import time

pygame.init()

# Open a new window
size = (1000, 750)
screen = pygame.display.set_mode(size)

sub_step = 2
frameRate = 60

dt = 2

class Engine_test:
    def __init__(self):
        pass

class VerletObject():
    def __init__(self, x, y, vx, vy):
        self.pos = pygame.Vector2(x, y)
        self.old_pos = pygame.Vector2(x, y-1)
        self.acceleration = pygame.Vector2(vx / frameRate, vy / frameRate)

        self.friction = 0.97
        self.groundfriction = 0.7

        self.coord_in_grid = [0, 0]

        self.radius = 2
        self.color = (0, 255, 0)
        self.mass = 1

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
        dist = math.dist(self.pos, obj2.pos)
        min_radius = self.radius + obj2.radius
        if (dist < min_radius):
            n = collision_axis/dist
            delta = min_radius - dist
            self.pos = self.pos + 0.5 * delta * n
            obj2.pos = obj2.pos - 0.5 * delta * n

    def draw(self):
        pygame.draw.circle(screen, (0, 255, 255), self.pos, self.radius)

dot1 = VerletObject(500, 200, 1, 1)
dot2 = VerletObject(100, 200, 1, 1)

dots = []
grid = {}
grid_size = 5
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

dotsNumber = 500
spawnRate = 1
spawnTimer = 1

check = []

clock = pygame.time.Clock()

while not exit:
    screen.fill((0, 0, 0))

    if spawnTimer == 0 and dotsNumber != 0:
        dots.append(VerletObject(500, 400, 1, 1))
        dotsNumber -= 1
        spawnTimer = spawnRate

    for step in range(0, sub_step):

        for index, x in enumerate(dots):
            x.accelerate(gravity)
            x.update()
            x.constraint_circle(300, 500, 300)

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

    pygame.display.set_caption(str(clock.get_fps()))
    spawnTimer -= 1
    pygame.display.update()
    time.sleep(1/frameRate)

    clock.tick(60)