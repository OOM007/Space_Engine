import os
import time

import pygame
import sys


pygame.init()

screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("test")

font = pygame.font.SysFont(None, 24)

class Button:
    def __init__(self, screen, position, size, List, buttonText=''):
        self.screen = screen
        self.position = pygame.Vector2(position)
        self.size = pygame.Vector2(size)
        self.text = buttonText

        self.alreadyPressed = False

        self.fillCollors = {
            'normal' : (0, 250, 0),
            'hover' : (200, 250, 0),
            'pressed' : '',
        }

        List.append(self)

    def check_pressed(self):
        mousePressed = pygame.mouse.get_pressed()
        if mousePressed[0] and self.alreadyPressed == False:
            self.alreadyPressed = True
            return True

    def check_mouse(self):
        mousePos = pygame.Vector2(pygame.mouse.get_pos())

        if mousePos.x > self.position.x and mousePos.x < self.position.x+self.size.x:
            if mousePos.y > self.position.y and mousePos.y < self.position.y + self.size.y:
                return True

    def update(self):
        t1 = font.render(self.text, True, (255, 0, 0))
        sizeText = pygame.Vector2(t1.get_size())

        color = None
        if self.check_mouse():
            color = "hover"

            if self.check_pressed():
                return True

        else:
            color = "normal"
            if self.alreadyPressed:
                self.alreadyPressed = False

        pygame.draw.rect(self.screen, self.fillCollors[color], (self.position, self.size))
        self.screen.blit(t1, ((self.position+(self.size/2))-(sizeText/2)))


class MainMenu:
    def __init__(self, screen):
        self.screen = screen

        #lists of buttons
        self.buttons = []
        self.menu_buttons = []
        self.Saves_menu = []
        self.Saving_menu = []

        # additional parameters
        self.menu_opened = False
        self.load_menu_opened = False
        self.saving_menu_opened = False
        self.save_list_opened = False

        # buttons
        MenuBtn = Button(screen, (0, screen.get_height() - 50), (100, 50), self.buttons, buttonText="Menu")
        saveBtn = Button(screen, (screen.get_width() - 100, screen.get_height() - 50), (100, 50), self.buttons, buttonText="Save")

        LoadBtn = Button(screen, (screen.get_width()/2-50, screen.get_height()/2-25), (100, 50), self.menu_buttons, buttonText="Load system")

        NewSaveBtn = Button(screen, (screen.get_width()/2-200, screen.get_height()/2-25), (200, 50), self.Saving_menu, buttonText="New Saving")
        OldSaveBtn = Button(screen, (screen.get_width()/2, screen.get_height()/2-25), (200, 50), self.Saving_menu, buttonText="Old Saving")

    def screen_update(self, list_of_btn):
        for button in list_of_btn:
            if button.update() == True:
                return button.text

    def open_saves_menu(self, Save_dir):
        content = os.listdir(Save_dir)
        closeBtn = Button(self.screen, (self.screen.get_width()/2-100, self.screen.get_height()/2-75), (200, 50), self.Saves_menu, buttonText="close")
        for index, data in enumerate(content):
            btn = Button(self.screen, (self.screen.get_width()/2-100, self.screen.get_height()/2+(51*index)), (200, 50), self.Saves_menu, buttonText=data)
            btn.alreadyPressed = True

    def close_saves_menu(self):
        self.Saves_menu.clear()