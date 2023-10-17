import random
import time

import numpy
import numpy as np
import pygame
import math
import matplotlib.pyplot as plt

# get other functions
import Body_Functions
from Engine_controle import Engine as Engine
from Engine_controle import Camera as Camera
from Text_controle_main import Text_controle
from Body_Functions import *

pygame.init()
font = pygame.font.SysFont(None, 24)

# Open a new window
size = (1000, 750)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("test")

GraviConst = 6.674 * 10**-11
print(GraviConst)

timeSpeed = 1000
scale = 100_000

trail_lenght = 20

# simple planet mass
Sun = 1.9885 * 10**30
jupiter = 1.898 * 10**27
earth = 5.9737 * 10**24

# simple planet distance
earth_sun = 1.5 * 10**11

# list initiating
planet_list = []

# parameters for optimizating
min_sim_mass = 500

clock = pygame.time.Clock()
frames = 0
simulation_time = 0

FindX = 0
FindY = 0

#[Position, scale, speed of move, speed of scale]
#Camera = Camera([0, 0, 0], 1*10**6, 1*10**11, 1*10**5)
#Camera for small simulations
Camera = Camera([0, 0, 0], 1, 10, 1)
Text_controle = Text_controle(screen)
Engine = Engine(1, 10)

#planet initiating
#body_1 = Planet((0, 0, 0), (0, 0, 0), 10**10, "star", 10, "1")
#body_2 = Planet((50, 0, 0), (0, -0.1108873302050329, 0), 567, "planet", 3, "2")
#body_3 = Planet((100, 0, 0), (0, -0.08, 0), 554, "planet", 3, "3")
#body_4 = Planet((200, 0, 0), (0, 0.04, 0), 89, "comet", 1, "4")
#body_5 = Planet((1000, 0 ,0), (0, -0.02, 0), 476, "planet", 3, "5")
#body_6 = Planet((4000, 0 ,0), (0, -0.003, 0), 687, "comet", 3, "6")

#body_1 = Planet((0, 0, 0), (0, 0, 0), 5.973*10**24, "star", 6371000, "1")
#body_2 = Planet((363104000, 0, 0), (0, 1023, 0), 7.347*10**22, "moon", 1737000, "2")

#body_1 = Planet((20, 0, 0), (0, 0, 0), 100_000_000, "star", 5, "1")
#body_2 = Planet((0, 0, 0), (-0.1, 0, 0), 100_000_0, "planet", 3, "2")

#testBody1 = Planet((0, 0, 0), (0, 0, 0), Sun, "star", 696*10**6, "Sun")
#testBody2 = Planet((0, 150*10**9, 0), (29780, 0, 0), earth, "planet", 6944*10**3, "Earth")
#testBody3 = Planet((0, 150.3844*10**9), (30803, 0, 0), 7.3477*10**22, "moon", 3400*10**3, "Moon")

#Engine.get_circle_coords(body_2.position[0], body_2.position[1], body_2.size)

#Calculating of orbit
#targetBody = body_2
#OrbitData = Engine.KeplersMaths(body_1.mass, math.sqrt(targetBody.vector[0]**2+targetBody.vector[1]**2), targetBody.mass, targetBody.position[0], 1943)

#CentrePos = ((targetBody.position[0]-OrbitData[3]), 0)

#test
trails = []
#testBody2 = Planet((0, 50, 0), (0, 0, 0), 10*10**9, "planet", 5, "Earth")
squaare = 5
tID = 0
for b in range(0, squaare):
    for p in range(0, squaare):
        test_body = Planet((p*10, b*10, 0), (0, 0, 0), 100000000, "planet", 1, str(tID), Engine, Camera)
        tID += 1


#follow function control
follow = False
followObj = None

#draw parametrs for future engine upgrades
vector_draw = False

#trail drawing parameter (base on)
trail_draw = False
orbit_draw = False

help_window = True

#simulation pause by stoping of calculating processes
pause = False

lists = []

#collect data settings [On/Off, seconds, body, second_body(if need), mode]
#modes - speed, dist to body (dist), gravitation influance (G_infl)
collectData = (False, 70000, "4", "4", "speed")

#body_2.create_particles()
#print(len(body_2.particleList))
#len_of_check = len(body_2.particleList)
#test = False

#for p in range(0, len_of_check):
#    if test:
#        body_2.particleList[1].stable_controle()
#    else:
#        test = body_2.particleList[0].stable_controle()

#print(len(body_2.particleList))

#list for data init
if collectData[4] == "G_infl":
    for x in range (0, len(planet_list)-1):
        lists.append([])
else:
    lists.append([])

while True:
    screen.fill((0, 0, 0))

    planet_list = Body_Functions.planet_list

    for body in planet_list:
        ID = body.ID
        if pause != True:
            for x in range(0, Engine.time_speed):
                for index, objects in enumerate(planet_list):
                    if objects.ID != ID:
                        collide = Engine.collision_detector(body, objects)
                        if objects.mass > min_sim_mass:
                            if collide:
                                pass
                            else:
                                gVector = Engine.VectorMath(body, objects)
                                body.vector = (body.vector[0] + gVector[0][0], body.vector[1] + gVector[0][1], 0)

                            if body.particleList:
                                for x in body.particleList:
                                    x.vector = body.vector

                            #collect data for graph
                            if ID == collectData[2] and collectData[0]:
                                if collectData[4] == "speed":
                                    lists[0].append(math.sqrt(body.vector[0] ** 2 + body.vector[1] ** 2))
                                elif collectData[4] == "dist":
                                    if objects.ID == collectData[3]:
                                        lists[0].append(gVector[1])
                                elif collectData[4] == "G_infl":
                                    if index==0:
                                        step = 0
                                    else:
                                        step = index-1

                                    lists[step].append(math.sqrt(gVector[0][0] ** 2 + gVector[0][1] ** 2))

            if body.particleList:
                for x in body.particleList:
                    x.update_pos()
            body.position = (body.position[0] - body.vector[0]*Engine.time_speed, body.position[1] - body.vector[1]*Engine.time_speed, 0)

        #for x in planet_list:
        #    if x.ID != ID:
        #        Engine.test(body, x)

        if trail_draw:
            body.trail_control(screen, frames, trail_lenght)

        if body.type != "star" and orbit_draw:
            body.orbit_draw_conrtole(screen)

        if body.particleList:
            for x in body.particleList:
                x.draw(Camera, screen)
        else:
            body.draw(screen, vector_draw)

    #text render
    if help_window:
        Text_controle.help_textRender()
    else:
        Text_controle.function_textRender(follow, vector_draw, trail_draw)
        if follow:
            Text_controle.planet_characteristics(planet_list[followObj], simulation_time)
        else:
            Text_controle.baseTextRender(simulation_time, (FindX, FindY), Camera, Engine)

    #key and other function control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_MINUS:
                if Camera.scale > Camera.speed_of_scale:
                    Camera.scale -= Camera.speed_of_scale
                elif Camera.scale > 0:
                    Camera.scale -= Camera.speed_of_scale/10
            if event.key == pygame.K_EQUALS:
                if Camera.scale >= Camera.speed_of_scale:
                    Camera.scale += Camera.speed_of_scale
                else:
                    Camera.scale += Camera.speed_of_scale/10

            #follow on function
            if event.key == pygame.K_f:
                if follow:
                    follow = False
                    followObj = None
                else:
                    follow = True
                    followObj = 0

            #vector draw on function
            if event.key == pygame.K_v:
                if vector_draw:
                    vector_draw = False
                else:
                    vector_draw = True

            if event.key == pygame.K_h:
                if help_window:
                    help_window = False
                else:
                    help_window = True

            #trail display on function
            if event.key == pygame.K_t:
                if trail_draw:
                    trail_draw = False
                else:
                    trail_draw = True

            if event.key == pygame.K_o:
                if orbit_draw:
                    orbit_draw = False
                else:
                    orbit_draw = True

            #pause controle
            if event.key == pygame.K_SPACE:
                if pause:
                    pause = False
                else:
                    pause = True

            #Time control
            if event.key == pygame.K_q:
                if Engine.time_speed > Engine.change_speed:
                    Engine.time_speed -= Engine.change_speed

            if event.key == pygame.K_e:
                Engine.time_speed += Engine.change_speed

            if event.key == pygame.K_RIGHT:
                if follow and followObj<len(planet_list)-1:
                    followObj+=1
                else:
                    Camera.move((-1, 0, 0))
            if event.key == pygame.K_LEFT:
                if follow and followObj!=0:
                    followObj-=1
                else:
                    Camera.move((1, 0, 0))
            if event.key == pygame.K_UP:
                Camera.move((0, 1, 0))
            if event.key == pygame.K_DOWN:
                Camera.move((0, -1, 0))

    if follow:
        Camera.follow(planet_list[followObj].position)

    if simulation_time >= collectData[1]:
        if collectData[0]:
            graph_time = np.arange(0, collectData[1])
            for x in range(0, len(lists)):
                print("work")
                plt.plot(lists[x])
            #plt.axis([0, collectData[1], 0.05, 0.1])
            plt.ylabel("speed in m/s")
            plt.show()
            break

    #print("________________")
    pygame.display.update()
    frames+=1
    if pause != True:
         simulation_time += Engine.time_speed
    time.sleep(0.1)