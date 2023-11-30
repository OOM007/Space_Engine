import os
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
import Collide_detect
from Saving_controle import Load
from Menu_control import MainMenu

Collide = Collide_detect.Collide()

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

def GetData(body, obj, gVector):
    # collect data for graph
    if body.ID == collectData[2] and collectData[0]:
        if collectData[4] == "speed":
            lists[0].append(math.sqrt(body.vector[0] ** 2 + body.vector[1] ** 2))
        elif collectData[4] == "dist":
            if obj.ID == collectData[3]:
                lists[0].append(gVector[1])

def MainCycle():
    if pause == False:
        for x in range(0, Engine.time_speed):
            checked = []
            for body in planet_list:
                for index, obj in enumerate(planet_list):
                    if body.ID != obj.ID:
                        grav = Engine.VectorMath(body, obj)
                        body.grav_vector = grav[0]
                        body.vector = body.vector - grav[0]

                        # collision detection
                        if Collide.collision_detect(body, obj) and obj not in checked:
                            Collide.collision(body, obj)

                body.position = body.position + body.vector
                checked.append(body)

    for b in planet_list:

        if trail_draw:
            b.trail_control(screen, frames, trail_lenght)

        if b.type != "star" and orbit_draw:
            b.orbit_draw_conrtole(screen)

        b.draw(screen, vector_draw)

#[Position, scale, speed of move, speed of scale]
#Camera = Camera([0, 0, 0], 1*10**6, 1*10**11, 1*10**5)
#Camera for small simulations
Camera = Camera([0, 0, 0], 1, 10, 1)
Text_controle = Text_controle(screen)
Engine = Engine(1, 1)
MainMenu = MainMenu(screen)

#collect data settings [On/Off, seconds, body, second_body(if need), mode]
#modes - speed, dist to body (dist), gravitation influance (G_infl)
collectData = (False, 70000, "4", "4", "speed")

trails = []
lists = []
square = 0
for x in range(0, square):
    for y in range(0, square):
        new_planet = Planet((x*25, y*25, 0), (0, 0, 0), 10**5, "planet", 2, str(x*5+y), Engine, Camera)

#list for data init
if collectData[4] == "G_infl":
    for x in range (0, len(planet_list)-1):
        lists.append([])
else:
    lists.append([])

run = True
simulation_run = False
menu_ans = None
ans = None

while run:
    screen.fill((0, 0, 0))

    # main simulation cycle
    if simulation_run:
        MainCycle()

    # menu cycle
    ans = MainMenu.screen_update(MainMenu.buttons)

    if MainMenu.menu_opened:
        menu_ans = MainMenu.screen_update(MainMenu.menu_buttons)
    elif MainMenu.save_list_opened:
        menu_ans = MainMenu.screen_update(MainMenu.Saves_menu)
    elif MainMenu.saving_menu_opened:
        menu_ans = MainMenu.screen_update(MainMenu.Saving_menu)

    # text render
    if help_window:
        Text_controle.help_textRender()
    else:
        Text_controle.function_textRender(follow, vector_draw, trail_draw)
        if follow:
            Text_controle.planet_characteristics(planet_list[followObj], simulation_time)
        else:
            Text_controle.baseTextRender(simulation_time, (FindX, FindY), Camera, Engine)

    # key and other function control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_MINUS:
                if Camera.scale > Camera.speed_of_scale:
                    Camera.scale -= Camera.speed_of_scale
                elif Camera.scale > 0:
                    Camera.scale -= Camera.speed_of_scale / 10
            if event.key == pygame.K_EQUALS:
                if Camera.scale >= Camera.speed_of_scale:
                    Camera.scale += Camera.speed_of_scale
                else:
                    Camera.scale += Camera.speed_of_scale / 10

            # follow on function
            if event.key == pygame.K_f:
                if follow:
                    follow = False
                    followObj = None
                else:
                    follow = True
                    followObj = 0

            # vector draw on function
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

            # trail display on function
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

            # pause controle
            if event.key == pygame.K_SPACE:
                if pause:
                    pause = False
                else:
                    pause = True

            # Time control
            if event.key == pygame.K_q:
                if Engine.time_speed > Engine.change_speed:
                    Engine.time_speed -= Engine.change_speed

            if event.key == pygame.K_e:
                Engine.time_speed += Engine.change_speed

            if event.key == pygame.K_RIGHT:
                if follow and followObj < len(planet_list) - 1:
                    followObj += 1
                else:
                    Camera.move((-1, 0, 0))
            if event.key == pygame.K_LEFT:
                if follow and followObj != 0:
                    followObj -= 1
                else:
                    Camera.move((1, 0, 0))
            if event.key == pygame.K_UP:
                Camera.move((0, 1, 0))
            if event.key == pygame.K_DOWN:
                Camera.move((0, -1, 0))

    # main menu check
    if ans != None:
        if ans == "Save" and simulation_run:
            opened = MainMenu.saving_menu_opened
            if opened:
                MainMenu.saving_menu_opened = False
            else:
                MainMenu.saving_menu_opened = True

        if ans == "Menu":
            opened = MainMenu.menu_opened
            if opened:
                print("closing menu...")
                MainMenu.menu_opened = False
            else:
                print("opening menu...")
                MainMenu.menu_opened = True

    # additional menu check
    if menu_ans != None:
        if menu_ans == "New Saving" and MainMenu.saving_menu_opened:
            print("creating new saving file...")

            content = os.listdir("Saves")
            fd = "Saves/Save_{0}.json".format(len(content)+1)
            Load.save_controle(Load, planet_list, fd)

            print(f"file \f{fd} created")

        elif menu_ans == "Old Saving" and MainMenu.saving_menu_opened:
            MainMenu.saving_menu_opened = True
            MainMenu.save_list_opened = True
            MainMenu.open_saves_menu("Saves")

        if menu_ans != None and MainMenu.save_list_opened and MainMenu.saving_menu_opened:
            if menu_ans != "close" and menu_ans != "Old Saving":
                # closing menu
                MainMenu.saving_menu_opened = False
                MainMenu.save_list_opened = False
                MainMenu.close_saves_menu()

                file_to_rewrite = "Saves/{0}".format(menu_ans)
                data = Load.save_controle(Load, planet_list, file_to_rewrite)

                print("file {0} rewrited".format(file_to_rewrite))
                pause = True

        if menu_ans != None and MainMenu.save_list_opened and MainMenu.saving_menu_opened == False:
            if menu_ans != "close" and menu_ans != "Load system":
                print(f"file \f{menu_ans} need to load")

                # closing all menu
                MainMenu.menu_opened = False
                MainMenu.save_list_opened = False
                MainMenu.close_saves_menu()

                file_to_load = "Saves/{0}".format(menu_ans)
                data = Load.load_file(Load, file_to_load)
                planet_list = Load.config_with_file(Load, data, Engine, Camera)
                print(planet_list)

                print(f"loading finished\n"
                      f"\f{len(planet_list)} planets loaded ")

                pause = True
                simulation_run = True

        if menu_ans == "Load system":
            MainMenu.save_list_opened = True
            MainMenu.menu_opened = False
            MainMenu.open_saves_menu("Saves")

        if menu_ans == "close" and MainMenu.save_list_opened:
            MainMenu.save_list_opened = False
            MainMenu.close_saves_menu()

    if follow:
        Camera.follow(planet_list[followObj].position)

    if simulation_time >= collectData[1]:
        if collectData[0]:
            graph_time = np.arange(0, collectData[1])
            for x in range(0, len(lists)):
                print("work")
                plt.plot(lists[x])
            # plt.axis([0, collectData[1], 0.05, 0.1])
            plt.ylabel("speed in m/s")
            plt.show()
            run = False

    # print("________________")
    pygame.display.update()
    frames += 1

    if pause != True and simulation_run:
        simulation_time += Engine.time_speed

    time.sleep(0.01)