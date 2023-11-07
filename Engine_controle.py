import numpy as np
import math
import pygame


GraviConst = 6.674 * 10**-11

class Camera:
    def __init__(self, position, scale, speed_of_move, speed_of_scale):
        self.position = position
        self.scale = scale
        self.speed_of_move = speed_of_move
        self.speed_of_scale = speed_of_scale

    def move(self, move_vector):
        #move vector example - (0, 0, 0)
        self.position[0] += self.speed_of_move*move_vector[0]
        self.position[1] += self.speed_of_move*move_vector[1]
        self.position[2] += self.speed_of_move*move_vector[2]

    def follow(self, obj_pos):
        self.position = [obj_pos[0], obj_pos[1], 0]

class Engine:
    def __init__(self, time_speed, change_speed):
        self.time_speed = time_speed
        self.change_speed = change_speed

    def gravitation_math(self, main_mass, m1, r):
        Force = GraviConst * ((m1 * main_mass) / r ** 2)
        acceleration = GraviConst * (m1 / r ** 2)
        HillRadius = r * (main_mass / (3 * (m1 + main_mass))) ** (1 / 3)
        a = Force / main_mass
        return Force, acceleration, HillRadius, a

    def VectorMath(self, Obj1, Obj2):
        pos1 = Obj1.position
        pos2 = Obj2.position

        DistVector = (pos1 - pos2)
        Dist = math.sqrt(DistVector[0] ** 2 + DistVector[1] ** 2)

        grav = self.gravitation_math(Obj1.mass, Obj2.mass, Dist)
        gravVector = pygame.Vector2(DistVector[0] / (Dist / grav[1]), DistVector[1] / (Dist / grav[1]))
        Obj1.grav_vector = gravVector

        return gravVector, Dist

    def get_circle_coords(self, cx, cy, r):
        coords = []
        for y in range(int(-r), int(+r+1)):
            x = (r**2 - y**2)**0.5

            x1 = -x + cx
            x2 = +x + cx

            y = y + cy

            coords.append([[x1, y], [x2, y]])
        return coords

    def test(self, b1, b2):
        dist = math.sqrt((b1.position[0]-b2.position[0])**2+(b1.position[1]-b2.position[1])**2) - (b1.size+b2.size)
        if dist < 0:
            diff = (b1.size+b2.size) - dist
            ratio = diff/dist
            move_x = (b1.position[0]-b2.position[0])/ratio
            move_y = (b1.position[1]-b2.position[1])/ratio

            b1.position = (b1.position[0] - (move_x / 2), b1.position[1] - (move_y / 2))
            b2.position = (b2.position[0] + (move_x / 2), b2.position[1] + (move_y / 2))


    def collision_reset(self, listOfPlanet):
        for x in listOfPlanet:
            x.CollideInProcess = False

    def find_E(self, M, r, initial_guess, tolerance=1e-6, max_iterations=100):
        E = initial_guess
        for i in range(max_iterations):
            f = E - r * math.sin(E) - M
            df = 1 - r * math.cos(E)
            E -= f / df
            if abs(f) < tolerance:
                return E
        return None

    def KeplersMaths(self, StarMass, planetSpeed, planetMass, periapsis, time):
        print("parametrs that given - ", StarMass, planetMass, planetSpeed, periapsis, time)
        majorA = abs(1 / ((2 / periapsis) - (planetSpeed ** 2 / (GraviConst * StarMass))))
        eccentricity = -((periapsis/majorA) - 1)
        majorB = majorA*math.sqrt(1-eccentricity**2)
        Period = (2 * math.pi) * math.sqrt((majorA ** 3) / (StarMass * GraviConst))
        print("Period", Period)
        print("eccentricity", eccentricity)

        meanMotion = (math.pi * 2) / Period
        meanAnomaly = meanMotion * time
        eccentricAnomaly = self.find_E(meanAnomaly, eccentricity, 0.0)
        trueAnomaly = 2 * math.atan(math.sqrt((1 + eccentricity) / (1 - eccentricity)) * math.tan(eccentricAnomaly / 2))
        heliocentricDist = periapsis * (1 - eccentricity * math.cos(eccentricAnomaly))

        planetX = heliocentricDist * math.cos(trueAnomaly)
        planetY = heliocentricDist * math.sin(trueAnomaly)

        print("planet x-{0} and y-{1} in {2}".format(planetX, planetY, time))

        #additional parametrs
        Aphelion = (1 + eccentricity) * majorA
        #Velocity if eccentrycity 0
        Vis_Viva = math.sqrt(GraviConst*StarMass*((2/periapsis)-(1/majorA)))
        VifE0 = math.sqrt((GraviConst*StarMass)/majorA)

        print("mean motion", VifE0)
        print("Aphelion, if eccentricity -x Periapsis - ", Aphelion)

        print("_______________")

        return planetX, planetY, Period, majorA, majorB