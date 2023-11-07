import pygame
import math

pygame.init()
font = pygame.font.SysFont(None, 24)

# color init
GREEN = (0, 255, 0)
class Text_controle:
    def __init__(self, screen):
        self.screen = screen

    def print_text(self, text, font, color, pos):
        printText = font.render(text, True, color)
        self.screen.blit(printText, pos)

    def help_textRender(self):
        self.print_text("Hello, this is early alpha version of space physic simulation", font, GREEN, (self.screen.get_width()/10, 0))
        self.print_text("For close this window press h, repeat if you want to see this again", font, GREEN, (self.screen.get_width()/10, 20))
        self.print_text("Press v to see vectors", font, GREEN, (self.screen.get_width()/10, 40))
        self.print_text("Press t to turn on/off planet trails", font, GREEN, (self.screen.get_width()/10, 60))
        self.print_text("Press f to turn on/off focus on planet, use arrow to change focus", font, GREEN, (self.screen.get_width()/10, 80))
        self.print_text("Use arrow to move camera", font, GREEN, (self.screen.get_width()/10, 100))
        self.print_text("Use +/- to scale perspective", font, GREEN, (self.screen.get_width()/10, 120))
        self.print_text("If you want to add new object, you only might to do this in code redactor for now", font, GREEN, (self.screen.get_width()/10, 140))
        self.print_text("For time forward use q/e", font, GREEN, (self.screen.get_width()/10, 160))

    def function_textRender(self, follow, vector_draw, trail_draw):
        followFunctioOn = font.render("follow on", True, (0, 255, 0))
        VectorFunctionOn = font.render("Vector display on", True, (0, 255, 0))
        trailDrawOn = font.render("Trail display on", True, (0, 255, 0))

        if follow:
            self.screen.blit(followFunctioOn, (self.screen.get_width() - 100, 20))
        if vector_draw:
            self.screen.blit(VectorFunctionOn, (self.screen.get_width() - 150, 40))
        if trail_draw:
            self.screen.blit(trailDrawOn, (self.screen.get_width() - 150, 60))

    def baseTextRender(self, simulation_time, FindXY, Camera, Engine):
        img3 = font.render("{0} seconds".format(simulation_time), True, (0, 255, 0))
        img4 = font.render("x-{0} y-{1}".format(FindXY[0], FindXY[1]), True, (0, 255, 0))
        cameraText = font.render("camera x-{0} y-{1}, camera scale {2}".format(Camera.position[0], Camera.position[1], Camera.scale), True, (0, 255, 0))
        TimeSpeedText = font.render("time speed {0}s/f".format(Engine.time_speed), True, (0, 255, 0))
        self.screen.blit(cameraText, (20, 10))
        self.screen.blit(img3, (20, 30))
        self.screen.blit(img4, (20, 50))
        self.screen.blit(TimeSpeedText, (20, 70))

    def planet_characteristics(self, planet, simulation_time):
        t1 = font.render("position x-{0} y-{1}".format(planet.position[0], planet.position[1]), True, (0, 255, 0))
        t2 = font.render("speed {0} m/s".format(math.sqrt(planet.vector[0]**2+planet.vector[1]**2)), True, (0, 255, 0))
        t3 = font.render("mass {0} kg".format(planet.mass), True, (0, 255, 0))
        t4 = font.render("radius {0} m".format(planet.size), True, (0, 255, 0))
        t5 = font.render("period of orit - {0} second".format(planet.OritPeriod), True, (0, 255, 0))
        t6 = font.render("ID - {0}".format(planet.ID), True, (0, 255, 0))
        img3 = font.render("{0} seconds".format(simulation_time), True, (0, 255, 0))

        self.screen.blit(t1, (20, 10))
        self.screen.blit(t2, (20, 30))
        self.screen.blit(t3, (20, 50))
        self.screen.blit(t4, (20, 70))
        self.screen.blit(t5, (20, 90))
        self.screen.blit(t6, (20, 110))
        self.screen.blit(img3, (20, 130))