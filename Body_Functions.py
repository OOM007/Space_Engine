import math
import pygame
from Parametrs import *

pygame.init()
font = pygame.font.SysFont(None, 24)

planet_list = []

class Particle:
    def __init__(self, parentBody, pos):
        self.parent = parentBody
        self.mass = parentBody.mass/parentBody.Ssize
        self.vector = parentBody.vector
        self.pos = pos

    def stable_controle(self, Engine):
        r = math.sqrt((self.parent.position[0] - self.pos[0]) ** 2 + (self.parent.position[1] - self.pos[1]) ** 2)
        if r == 0:
            return True
        else:
            pBody_infl = Engine.gravitation_math(self.mass, self.parent.mass, r)
            starBody_infl = Engine.gravitation_math(self.mass, self.parent.mass, math.sqrt((self.parent.position[0]-self.pos[0])**2+(self.parent.position[1]-self.pos[1])**2))

            if pBody_infl[0] < starBody_infl[0]:
                self.test_destroy()

    def draw(self, camera, screen):
        pygame.draw.circle(screen, (250, 0, 250), (
        ((screen.get_width() / 2) + ((camera.position[0] - self.pos[0]) / camera.scale)),
        (screen.get_width() / 2) + ((camera.position[1] - self.pos[1]) / camera.scale)), 0.5 / camera.scale)

    def update_pos(self, Engine):
        self.pos = (self.pos[0]-self.vector[0]*Engine.time_speed, self.pos[1]-self.vector[1]*Engine.time_speed, 0)

    def test_destroy(self):
        self.vector = (self.vector[0], self.vector[1], 0)

        new = Planet(self.pos, self.vector, self.mass, "particle", 0.5, str(len(planet_list)))

        new.fromParticle = True

        self.parent.mass -= self.mass

        self.parent.particleList.remove(self)

        if len(self.parent.particleList) == 0:
            del self.parent

        del self

    def __del__(self):
        pass

class Planet:
    def __init__(self, position, vector, mass, type, size, ID, Engine, Camera):
        self.Engine = Engine
        self.Camera = Camera

        self.fromParticle = False
        planet_list.append(self)

        #base parameters
        self.position = pygame.Vector2(position[0], position[1])
        self.old_position = pygame.Vector2(position[0]-vector[0], position[1]-vector[1])
        self.vector = pygame.Vector2(vector[0], vector[1])
        self.mass = mass
        self.type = type
        self.size = size
        self.ID = ID

        #additional parameters
        self.CollideInProcess = False
        self.Ssize = int(2*math.pi*size**2)
        self.particleList = []
        self.ParticleGen = False

        self.parent_body = planet_list[0]
        self.grav_vector = pygame.Vector2(0, 0)

        if type != "star" and orbitMaths:
            self.OrbitData = Engine.KeplersMaths(self.parent_body.mass, math.sqrt(self.vector[0]**2+self.vector[1]**2), self.mass, math.sqrt(self.position[0]**2+self.position[1]**2), 1000)
            self.CentrePos = ((self.position[0] - self.OrbitData[3]), 0)
            self.OritPeriod = self.OrbitData[2]
        else:
            self.OritPeriod = 0

        # drawing parametrs
        self.screen_position = None
        self.trail = []
        self.lbl = font.render(ID, True, (0, 0, 255))

    def update(self, dt):
        vel = self.position - self.old_position
        self.old_position = self.position
        self.position = self.position + vel + ((-self.grav_vector) * dt ** 2)

        self.vector = -vel

    def draw(self, screen, vector_draw):
        size_of_draw = self.size/self.Camera.scale
        self.screen_position = (((screen.get_width()/2)+((self.Camera.position[0]-self.position[0])/self.Camera.scale)), (screen.get_width()/2)+((self.Camera.position[1]-self.position[1])/self.Camera.scale))
        #drawing planet
        if size_of_draw >= 1:
            pygame.draw.circle(screen, (250, 250, 250), (self.screen_position[0], self.screen_position[1]), size_of_draw)
        else:
            screen.blit(self.lbl, (self.screen_position[0], self.screen_position[1]))

        #drawing force vector and gravitation force vector
        if vector_draw:
            pygame.draw.line(screen, (250, 250, 0), (self.screen_position[0], self.screen_position[1]), (self.screen_position[0]+self.vector[0]*1000/self.Camera.scale, self.screen_position[1]+self.vector[1]*1000/self.Camera.scale))
            pygame.draw.line(screen, (250, 0, 250), (self.screen_position[0], self.screen_position[1]), (self.screen_position[0]+self.grav_vector[0]*100000/self.Camera.scale, self.screen_position[1]+self.grav_vector[1]*100000/self.Camera.scale), 2)

    def create_particles(self):
        coords = self.Engine.get_circle_coords(self.position[0], self.position[1], self.size)
        for coord in coords:
            step = 1
            tx = 0
            ty = coord[0][1]
            while tx <= coord[1][0]:
                tx = coord[0][0] + step
                self.particleList.append(Particle(self, (tx, ty)))
                step+=1

    def test_draw(self, screen):
        coords = self.Engine.get_circle_coords(self.position[0], self.position[1], self.size)
        for index, coord in enumerate(coords):
            step = 1
            tx = 0
            ty = coord[0][1]

            while tx <= coord[1][0]:
                tx = coord[0][0] + step
                pygame.draw.circle(screen, (250, 0, 250), (((screen.get_width()/2)+((self.Camera.position[0]-tx)/self.Camera.scale)), (screen.get_width()/2)+((self.Camera.position[1]-ty)/self.Camera.scale)), 1/self.Camera.scale)
                step+=1

    def orbit_draw_conrtole(self, screen):
        Orbit_Draw = pygame.Rect(
            ((screen.get_width() / 2) + ((self.Camera.position[0] - (self.CentrePos[0] + self.OrbitData[3])) / self.Camera.scale)),
            (screen.get_width() / 2) + ((self.Camera.position[1] - (self.CentrePos[1] + self.OrbitData[4])) / self.Camera.scale)
            , (self.OrbitData[3] * 2) / self.Camera.scale, (self.OrbitData[4] * 2) / self.Camera.scale)
        pygame.draw.ellipse(screen, (255, 0, 0), Orbit_Draw, width=1)

    def trail_control(self, screen, frames, trail_lenght):
        trails_frame = frames / (100/self.Engine.time_speed)
        if trails_frame.is_integer():
            self.trail.append(self.position)
        if len(self.trail) > trail_lenght:
            self.trail.remove(self.trail[0])

        for index, coords in enumerate(self.trail):
            if len(self.trail) > 2 and index!= len(self.trail)-2:
                start_coords = ((screen.get_width()/2)+((self.Camera.position[0]-coords[0])/self.Camera.scale), (screen.get_width()/2)+((self.Camera.position[1]-coords[1])/self.Camera.scale))
                finish_coords = self.trail[index+1]
                finish_coords = ((screen.get_width()/2)+((self.Camera.position[0]-finish_coords[0])/self.Camera.scale), (screen.get_width()/2)+((self.Camera.position[1]-finish_coords[1])/self.Camera.scale))
                pygame.draw.line(screen, (0, 255, 0), (int(start_coords[0]), int(start_coords[1])), ((int(finish_coords[0])), int(finish_coords[1])))
            else:
                break

    def __del__(self):
        planet_list.remove(self)