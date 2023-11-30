import time
import pygame
import math


pygame.init()
font = pygame.font.SysFont(None, 24)

# Open a new window
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("test")

GraviConst = 6.674 * 10**-11
print(GraviConst)

timeSpeed = 1000
scale = 100_000

trail_lenght = 20

#simple planet mass
Sun = 1.9885 * 10**30
jupiter = 1.898 * 10**27
earth = 5.9737 * 10**24

#speed of origin earth 0.000029722

#Example of space body: Name = [coords, speedVector, mass, class, size]
# 1 unit of coordinate is 1 000 000 km
bodys = [
    [(150*10**9, 0, 0), (0, 2972_000, 0), earth, "planet", 100, "1"],
    [(0, 0, 0), (0, 0, 0), Sun, "star", 1000, "2"]
]

Earth_and_sattelite = [
    [(0, 0, 0), (0, 0, 0), earth, "planet", 6400000, "1"],
    [(-7700_000, 0, 0), (0, 8000, 0), 10, "sattelite", 10, "2"]
]

bodys_for_tests = [
    [(100, 0, 0), (0, 0.08, 0), 10**10, "star", 3, "1"],
    [(0, 0, 0), (0, -0.01, 0), 10**10, "star", 3, "2"]
]

#simple planet distance
earth_sun = 1.5 * 10**11

class Engine:
    def __init__(self):
        pass

    def gravitation_math(self, m1, m2, r):
        Force = GraviConst * ((m1 * m2) / r ** 2)
        acceleration = GraviConst * (m1 / r ** 2)
        HillRadius = r * (m2 / (3 * (m1 + m2))) ** (1 / 3)
        a = Force / m2
        return Force, acceleration, HillRadius, a

    def find_E(self, M, r, initial_guess, tolerance=1e-6, max_iterations=100):
        E = initial_guess
        for i in range(max_iterations):
            f = E - r * math.sin(E) - M
            df = 1 - r * math.cos(E)
            E -= f / df
            if abs(f) < tolerance:
                return E
        return None

    def VectorMath(Obj1, Obj2):
        pos1 = Obj1[0]
        pos2 = Obj2[0]

        DistVector = (pos1[0] - pos2[0], pos1[1] - pos2[1])
        Dist = math.sqrt(DistVector[0] ** 2 + DistVector[1] ** 2)

        grav = gravitation_math(Obj2[2], Obj1[2], Dist)
        gravVector = (DistVector[0] / (Dist / grav[1]), DistVector[1] / (Dist / grav[1]))

        return gravVector, Dist

    def KeplersMaths(StarMass, planetSpeed, planetMass, periapsis, time):
        print(StarMass, planetMass, planetSpeed, periapsis, time)
        majorA = abs(1 / ((2 / periapsis) - (planetSpeed ** 2 / (GraviConst * StarMass))))
        eccentricity = (majorA / periapsis) - 1
        print(majorA)
        Period = (2 * math.pi) * math.sqrt((majorA ** 3) / (StarMass * GraviConst))
        print(Period)
        print("eccentricity", eccentricity)

        meanMotion = (math.pi * 2) / Period
        meanAnomaly = meanMotion * time
        eccentricAnomaly = find_E(meanAnomaly, eccentricity, 0.0)
        trueAnomaly = 2 * math.atan(math.sqrt((1 + eccentricity) / (1 - eccentricity)) * math.tan(eccentricAnomaly / 2))
        heliocentricDist = periapsis * (1 - eccentricity * math.cos(eccentricAnomaly))

        planetX = heliocentricDist * math.cos(trueAnomaly)
        planetY = heliocentricDist * math.sin(trueAnomaly)

        Aphelion = (1 + eccentricity) * majorA

        print(Period, Aphelion)

        return planetX, planetY

class Camera:
    def __init__(self, position, scale, speed_of_move):
        self.position = position
        self.scale = scale
        self.speed_of_move = speed_of_move

    def move(self, move_vector):
        #move vector example - (0, 0, 0)
        self.position[0] += self.speed_of_move*move_vector[0]
        self.position[1] += self.speed_of_move*move_vector[1]
        self.position[2] += self.speed_of_move*move_vector[2]

class Planet:
    def __init__(self, position, vector, mass, type, size, ID):
        #base parameters
        self.position = position
        self.vector = vector
        self.mass = mass
        self.type = type
        self.size = size
        self.ID = ID

        #additional parameters
        self.parent_body = None

        # drawing parametrs
        self.trail = []

    def draw(self, camera):
        pygame.draw.circle(screen, (250 ,250 ,250),
                           (camera.position[0]-(self.position[0]/camera.scale)+(screen.get_width()/2), camera.position[1]-(self.position[1]/camera.scale)+(screen.get_width()/2)),
                           self.size)

    def trail_control(self):
        pass



def find_E(M, r, initial_guess, tolerance=1e-6, max_iterations=100):
    E = initial_guess
    for i in range(max_iterations):
        f = E - r * math.sin(E) - M
        df = 1 - r * math.cos(E)
        E -= f / df
        if abs(f) < tolerance:
            return E
    return None

def gravitation_math(m1, m2, r):
    Force = GraviConst*((m1*m2)/r**2)
    acceleration = GraviConst*(m1/r**2)
    HillRadius = r*(m2/(3*(m1 + m2)))**(1/3)
    a = Force/m2
    return Force, acceleration, HillRadius, a

def VectorMath (Obj1, Obj2):
    pos1 = Obj1[0]
    pos2 = Obj2[0]

    DistVector = (pos1[0] - pos2[0], pos1[1] - pos2[1])
    Dist = math.sqrt(DistVector[0]**2+DistVector[1]**2)

    grav = gravitation_math(Obj2[2], Obj1[2], Dist)
    gravVector = (DistVector[0]/(Dist/grav[1]), DistVector[1]/(Dist/grav[1]))

    return gravVector, Dist

def KeplersMaths(StarMass, planetSpeed, planetMass, periapsis, time):
    print(StarMass, planetMass, planetSpeed, periapsis, time)
    majorA = abs(1/((2/periapsis)-(planetSpeed**2/(GraviConst*StarMass))))
    eccentricity = (majorA/periapsis)-1
    print(majorA)
    Period = (2*math.pi)*math.sqrt((majorA**3)/(StarMass*GraviConst))
    print(Period)
    print("eccentricity", eccentricity)

    meanMotion = (math.pi*2)/Period
    meanAnomaly = meanMotion*time
    eccentricAnomaly = find_E(meanAnomaly, eccentricity, 0.0)
    trueAnomaly = 2*math.atan(math.sqrt((1+eccentricity)/(1-eccentricity))*math.tan(eccentricAnomaly/2))
    heliocentricDist = periapsis*(1-eccentricity*math.cos(eccentricAnomaly))

    planetX = heliocentricDist*math.cos(trueAnomaly)
    planetY = heliocentricDist*math.sin(trueAnomaly)

    Aphelion = (1+eccentricity)*majorA

    print(Period, Aphelion)

    return planetX, planetY

prediction = KeplersMaths(Earth_and_sattelite[0][2], Earth_and_sattelite[1][1][1], 10, abs(Earth_and_sattelite[1][0][0]), 1000)
clock = pygame.time.Clock()
frames = 0

print("Predicted x-{0}, predicted y-{1}".format(prediction[0], prediction[1]))

FindX = 0
FindY = 0

#planet initiating


Camera = Camera([0, 0, 0], 1, 10)

#test
trails = []

while True:
    screen.fill((0, 0, 0))

    for body in bodys_for_tests:
        ID = body[5]
        for objects in bodys_for_tests:
            if objects[5]!=ID:
                gVector = VectorMath(body, objects)

                body[1] = (body[1][0] + gVector[0][0], body[1][1] + gVector[0][1], 0)
                body[0] = (body[0][0] - body[1][0], body[0][1] - body[1][1], 0)

        # drawing trajectory
        if frames == 0:
            trails.append([])
        trails_frame = frames/100
        if trails_frame.is_integer():
            trails[int(ID)-1].append(body[0])
        if len(trails[int(ID)-1]) > trail_lenght:
            trails[int(ID)-1].remove(trails[int(ID)-1][0])

        #drawing lines
        for index, coords in enumerate(trails[int(ID)-1]):
            if len(trails[int(ID)-1]) > 2 and index!= len(trails[int(ID)-1])-2:
                start_coords = (Camera.position[0]-(coords[0]/Camera.scale)+(screen.get_width()/2), Camera.position[1]-(coords[1]/Camera.scale)+(screen.get_width()/2))
                finish_coords = trails[int(ID)-1][index+1]
                finish_coords = (Camera.position[0]-(finish_coords[0]/Camera.scale)+(screen.get_width()/2), Camera.position[1]-(finish_coords[1]/Camera.scale)+(screen.get_width()/2))
                pygame.draw.line(screen, (0, 255, 0), (int(start_coords[0]), int(start_coords[1])), ((int(finish_coords[0])), int(finish_coords[1])))
            else:
                break
                
        size = body[4] / scale
        if size < 1:
            size = 1

        pygame.draw.circle(screen, (250, 250, 250),
                           (Camera.position[0]-(body[0][0]/Camera.scale)+(screen.get_width()/2), Camera.position[1]-(body[0][1]/Camera.scale)+(screen.get_width()/2)), size)

    txtDist = int(gVector[1])
    txtSpeed = int(math.sqrt(body[1][0] ** 2 + body[1][1] ** 2))
    img1 = font.render('{0} m'.format(txtDist), True, (0, 255, 0))
    img2 = font.render("{0} m/s".format(txtSpeed), True, (0, 255, 0))
    img3 = font.render("{0} frame".format(frames), True, (0, 255, 0))
    img4 = font.render("x-{0} y-{1}".format(FindX, FindY), True, (0, 255, 0))
    screen.blit(img1, (20, 20))
    screen.blit(img2, (20, 40))
    screen.blit(img3, (20, 60))
    screen.blit(img4, (20, 80))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_MINUS:
                if Camera.scale > 1:
                    Camera.scale -= 1
            if event.key == pygame.K_EQUALS:
                Camera.scale += 1

            if event.key == pygame.K_RIGHT:
                Camera.move((-1, 0, 0))
            if event.key == pygame.K_LEFT:
                Camera.move((1, 0, 0))
            if event.key == pygame.K_UP:
                Camera.move((0, 1, 0))
            if event.key == pygame.K_DOWN:
                Camera.move((0, -1, 0))

    if frames == 1000:
        FindX = Earth_and_sattelite[1][0][0]
        FindY = Earth_and_sattelite[1][0][1]
    #print("________________")
    pygame.display.update()
    frames+=1
    time.sleep(0.01)