import time
import numpy as np
import matplotlib.pyplot as plt

# get other functions
import pygame

import Body_Functions
from Engine_controle import Engine as Engine
from Engine_controle import Camera as Camera
from Text_controle_main import Text_controle
from Body_Functions import *
from Parametrs import *

pygame.init()
font = pygame.font.SysFont(None, 24)

# Open a new window
size = (1000, 750)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("test")

# list initiating
planet_list = []

clock = pygame.time.Clock()
frames = 0
simulation_time = 0

FindX = 0
FindY = 0


def mainCycle():
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
                                body.vector = body.vector + gVector[0]

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

            body.position = body.position - body.vector*Engine.time_speed

        if trail_draw:
            body.trail_control(screen, frames, trail_lenght)

        if body.type != "star" and orbit_draw:
            body.orbit_draw_conrtole(screen)

        if body.particleList:
            for x in body.particleList:
                x.draw(Camera, screen)
        else:
            body.draw(screen, vector_draw)

def testMainCycle():
    for x in range(0, Engine.time_speed):
        checked = []
        for body in planet_list:
            for obj in planet_list:
                # Checked or Not
                CorN = obj in checked
                if body.ID != obj.ID and CorN != True:
                    collided = Engine.collision(body, obj)
                    if collided != True:
                        grav = Engine.VectorMath(body, obj)
                        grav2 = Engine.VectorMath(obj, body)
                        body.grav_vector = grav[0]
                        obj.grav_vector = grav2[0]

                    body.update(1)
                    obj.update(1)

            checked.append(body)
    for b in planet_list:
        b.draw(screen, vector_draw)


#[Position, scale, speed of move, speed of scale]
#Camera = Camera([0, 0, 0], 1*10**6, 1*10**11, 1*10**5)
#Camera for small simulations
Camera = Camera([0, 0, 0], 1, 10, 1)
Text_controle = Text_controle(screen)
Engine = Engine(1, 10)

#planet initiating
#body_1 = Planet((0, 0, 0), (0, 0, 0), 10**10, "star", 10, "1", Engine, Camera)
#body_2 = Planet((50, 0, 0), (0, 0, 0), 567, "planet", 3, "2", Engine, Camera)
#body_3 = Planet((100, 0, 0), (0, -0.08, 0), 554, "planet", 3, "3")
#body_4 = Planet((200, 0, 0), (0, 0.04, 0), 89, "comet", 1, "4")
#body_5 = Planet((1000, 0 ,0), (0, -0.02, 0), 476, "planet", 3, "5")
#body_6 = Planet((4000, 0 ,0), (0, -0.003, 0), 687, "comet", 3, "6")

#body_1 = Planet((0, 0, 0), (0, 0, 0), 5.973*10**24, "star", 6371000, "1")
#body_2 = Planet((363104000, 0, 0), (0, 1023, 0), 7.347*10**22, "moon", 1737000, "2")

#body_1 = Planet((50, 0, 0), (-0.1, 0, 0), 100_000_000, "star", 5, "test_planet", Engine, Camera)
#body_2 = Planet((12, 0, 0), (0.1, 0, 0), 100_000_000, "planet", 3, "2", Engine, Camera)

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

square = 5
for x in range(0, square):
    for y in range(0, square):
        new_planet = Planet((x*10, y*10, 0), (0, 0, 0), 10**5, "planet", 2, str(x*5+y), Engine, Camera)

#list for data init
if collectData[4] == "G_infl":
    for x in range (0, len(planet_list)-1):
        lists.append([])
else:
    lists.append([])

run = True
while run:
    screen.fill((0, 0, 0))

    planet_list = Body_Functions.planet_list

    testMainCycle()
    #mainCycle()

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
            run = False

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