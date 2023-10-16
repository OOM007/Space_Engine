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

        self.radius = 5
        self.color = (0, 255, 0)
        self.mass = 1

    def update(self):
        vel = self.pos - self.old_pos
        self.old_pos = self.pos
        self.pos = self.pos + vel + self.acceleration * dt**2


        self.acceleration = pygame.Vector2(0, 0)

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
dot2 = VerletObject(500, 300, 1, 1)

dots = []
grid = []
grid_stepX = size[0]/20
grid_stepY = size[1]/20

print(grid)
dots.append(dot1)
dots.append(dot2)

exit = False

gravity = pygame.Vector2(0/frameRate, 1/frameRate)

Engine = Engine_test()

Collision = False

if len(dots) > 1:
    collision = True

dotsNumber = 1000
spawnRate = 1
spawnTimer = 1

check = []

while not exit:
    grid.clear()

    for y in range(0, int(grid_stepY)):
        grid.append([])
        for x in range(0, int(grid_stepX)):
            grid[y].append([])

    if spawnTimer == 0 and dotsNumber != 0:
        dots.append(VerletObject(500, 400, 1, 1))
        dotsNumber -= 1
        spawnTimer = spawnRate

    for step in range(0, sub_step):
        screen.fill((0, 0, 0))
        for dot in dots:
            grid_pos = pygame.Vector2(int(round(dot.pos.x/20)), int(round(dot.pos.y/20)))
            grid[int(grid_pos.x)][int(grid_pos.y)].append(dot)

            if len(grid[int(grid_pos.x)][int(grid_pos.y)]) > 1:
                check.append((grid_pos.x, grid_pos.y))

        # clear duplicates
        check = list(set(check))

        for index, x in enumerate(dots):
            x.accelerate(gravity)
            x.update()
            x.constraint_circle(300, 300, 300)

            grid_pos = ((int(round(x.pos.x/20))), int(round(x.pos.y/20)))

            if grid[grid_pos[0]][grid_pos[1]] == []:
                pass
            else:
                for obj in grid[grid_pos[0]][grid_pos[1]]:
                    if obj == x:
                        pass
                    else:
                        x.collision(obj)

            x.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

    spawnTimer -= 1
    pygame.display.update()
    time.sleep(1/frameRate)