import time
import pygame
import math


pygame.init()
font = pygame.font.SysFont(None, 24)

# Open a new window
size = (1000, 1000)
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

#simple planet distance
earth_sun = 1.5 * 10**11

# list initiating
planet_list = []

class Engine:
    def __init__(self, time_speed):
        self.time_speed = time_speed

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

class Text_controle:
    def __init__(self):
        pass
    def help_textRender(self):
        helpRander1 = font.render("Hello, this is early alpha version of space physic simulation", True, (0, 255, 0))
        helpRander2 = font.render("For close this window press h, repeat if you want to see this again", True, (0, 255, 0))
        helpRander3 = font.render("Press v to see vectors", True, (0, 255, 0))
        helpRander4 = font.render("Press t to turn on/off planet trails", True, (0, 255, 0))
        helpRander5 = font.render("Press f to turn on/off focus on planet, use arrow to change focus", True, (0, 255, 0))
        helpRander6 = font.render("Use arrow to move camera", True, (0, 255, 0))
        helpRander7 = font.render("Use +/- to scale perspective", True, (0, 255, 0))
        helpRander8 = font.render("If you want to add new object, you only might to do this in code redactor for now", True, (0, 255, 0))
        helpRender9 = font.render("Time forwarding will be added as soon as possible", True, (0, 255, 0))
        screen.blit(helpRander1, (screen.get_width()/10, 0))
        screen.blit(helpRander2, (screen.get_width() / 10, 20))
        screen.blit(helpRander3, (screen.get_width() / 10, 40))
        screen.blit(helpRander4, (screen.get_width() / 10, 60))
        screen.blit(helpRander5, (screen.get_width() / 10, 80))
        screen.blit(helpRander6, (screen.get_width() / 10, 100))
        screen.blit(helpRander7, (screen.get_width() / 10, 120))
        screen.blit(helpRander8, (screen.get_width() / 10, 140))
        screen.blit(helpRender9, (screen.get_width() / 10, 160))

    def function_textRender(self):
        followFunctioOn = font.render("follow on", True, (0, 255, 0))
        VectorFunctionOn = font.render("Vector display on", True, (0, 255, 0))
        trailDrawOn = font.render("Trail display on", True, (0, 255, 0))

        if follow:
            screen.blit(followFunctioOn, (screen.get_width() - 100, 20))
        if vector_draw:
            screen.blit(VectorFunctionOn, (screen.get_width() - 150, 40))
        if trail_draw:
            screen.blit(trailDrawOn, (screen.get_width() - 150, 60))

    def baseTextRender(self):
        img3 = font.render("{0} frame".format(frames), True, (0, 255, 0))
        img4 = font.render("x-{0} y-{1}".format(FindX, FindY), True, (0, 255, 0))
        cameraText = font.render("camera x-{0} y-{1}, camera scale {2}".format(Camera.position[0], Camera.position[1], Camera.scale), True, (0, 255, 0))
        TimeSpeedText = font.render("time speed {0}s/f".format(Engine.time_speed), True, (0, 255, 0))
        screen.blit(cameraText, (20, 10))
        screen.blit(img3, (20, 30))
        screen.blit(img4, (20, 50))
        screen.blit(TimeSpeedText, (20, 70))

    def planet_characteristics(self, planet):
        t1 = font.render("position x-{0} y-{1}".format(planet.position[0], planet.position[1]), True, (0, 255, 0))
        t2 = font.render("speed {0} m/s".format(math.sqrt(planet.vector[0]**2+planet.vector[1]**2)), True, (0, 255, 0))
        t3 = font.render("mass {0} kg".format(planet.mass), True, (0, 255, 0))
        t4 = font.render("radius {0} m".format(planet.size), True, (0, 255, 0))
        t5 = font.render("ID - {0}".format(planet.ID), True, (0, 255, 0))

        screen.blit(t1, (20, 10))
        screen.blit(t2, (20, 30))
        screen.blit(t3, (20, 50))
        screen.blit(t4, (20, 70))
        screen.blit(t5, (20, 90))


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

class Planet:
    def __init__(self, position, vector, mass, type, size, ID):
        planet_list.append(self)

        #base parameters
        self.position = position
        self.vector = vector
        self.mass = mass
        self.type = type
        self.size = size
        self.ID = ID

        #additional parameters
        self.parent_body = None
        self.grav_vector = ()

        # drawing parametrs
        self.screen_position = None
        self.trail = []
        self.lbl = font.render(ID, True, (0, 0, 255))

    def draw(self, camera):
        size_of_draw = self.size/camera.scale
        self.screen_position = (((screen.get_width()/2)+((camera.position[0]-self.position[0])/camera.scale)), (screen.get_width()/2)+((camera.position[1]-self.position[1])/camera.scale))
        #drawing planet
        if size_of_draw >=1:
            pygame.draw.circle(screen, (250, 250, 250), (self.screen_position[0], self.screen_position[1]), size_of_draw)
        else:
            screen.blit(self.lbl, (self.screen_position[0], self.screen_position[1]))

        #drawing force vector and gravitation force vector
        if vector_draw:
            pygame.draw.line(screen, (250, 250, 0), (self.screen_position[0], self.screen_position[1]), (self.screen_position[0]+self.vector[0]*1000/Camera.scale, self.screen_position[1]+self.vector[1]*1000/Camera.scale))
            pygame.draw.line(screen, (250, 0, 250), (self.screen_position[0], self.screen_position[1]), (self.screen_position[0]+self.grav_vector[0]*100000/Camera.scale, self.screen_position[1]+self.grav_vector[1]*100000/Camera.scale), 2)

    def trail_control(self):
        trails_frame = frames / (100/Engine.time_speed)
        if trails_frame.is_integer():
            self.trail.append(body.position)
        if len(self.trail) > trail_lenght:
            self.trail.remove(self.trail[0])

        for index, coords in enumerate(self.trail):
            if len(self.trail) > 2 and index!= len(self.trail)-2:
                start_coords = ((screen.get_width()/2)+((Camera.position[0]-coords[0])/Camera.scale), (screen.get_width()/2)+((Camera.position[1]-coords[1])/Camera.scale))
                finish_coords = self.trail[index+1]
                finish_coords = ((screen.get_width()/2)+((Camera.position[0]-finish_coords[0])/Camera.scale), (screen.get_width()/2)+((Camera.position[1]-finish_coords[1])/Camera.scale))
                pygame.draw.line(screen, (0, 255, 0), (int(start_coords[0]), int(start_coords[1])), ((int(finish_coords[0])), int(finish_coords[1])))
            else:
                break

    def gravitation_math(self, m1, r):
        Force = GraviConst * ((m1 * self.mass) / r ** 2)
        acceleration = GraviConst * (m1 / r ** 2)
        HillRadius = r * (self.mass / (3 * (m1 + self.mass))) ** (1 / 3)
        a = Force / self.mass
        return Force, acceleration, HillRadius, a

    def VectorMath(self, Obj2):
        pos1 = self.position
        pos2 = Obj2.position

        DistVector = (pos1[0] - pos2[0], pos1[1] - pos2[1])
        Dist = math.sqrt(DistVector[0] ** 2 + DistVector[1] ** 2)

        grav = body.gravitation_math(Obj2.mass, Dist)
        gravVector = (DistVector[0] / (Dist / grav[1]), DistVector[1] / (Dist / grav[1]))
        self.grav_vector = gravVector

        return gravVector, Dist

def find_E(M, r, initial_guess, tolerance=1e-6, max_iterations=100):
    E = initial_guess
    for i in range(max_iterations):
        f = E - r * math.sin(E) - M
        df = 1 - r * math.cos(E)
        E -= f / df
        if abs(f) < tolerance:
            return E
    return None

clock = pygame.time.Clock()
frames = 0

FindX = 0
FindY = 0

#planet initiating
body_1 = Planet((0, 0, 0), (0, -0.01, 0), 10**10, "star", 10, "1")
body_2 = Planet((50, 0, 0), (0, -0.1, 0), 10, "planet", 3, "2")
body_3 = Planet((100, 0, 0), (0, -0.06, 0), 10, "planet", 3, "3")
body_4 = Planet((200, 0, 0), (0, 0.04, 0), 2, "comet", 1, "4")
body_5 = Planet((1000, 0 ,0), (0, -0.02, 0), 3, "planet", 3, "5")

#testBody1 = Planet((0, 0, 0), (0, 0, 0), Sun, "star", 696*10**6, "Sun")
#testBody2 = Planet((0, 150*10**9, 0), (29780, 0, 0), earth, "planet", 696*10**6, "Earth")

Camera = Camera([0, 0, 0], 1, 10, 1)
Text_controle = Text_controle()
Engine = Engine(1)

#test
trails = []

#follow function control
follow = False
followObj = None

#draw parametrs for future engine upgrades
vector_draw = False

#trail drawing parameter (base on)
trail_draw = False

help_window = True

while True:
    screen.fill((0, 0, 0))

    for body in planet_list:
        ID = body.ID
        for x in range(0, Engine.time_speed):
            for objects in planet_list:
                if objects.ID != ID:
                    gVector = body.VectorMath(objects)

                    body.vector = (body.vector[0] + gVector[0][0], body.vector[1] + gVector[0][1], 0)

        body.position = (body.position[0] - body.vector[0]*Engine.time_speed, body.position[1] - body.vector[1]*Engine.time_speed, 0)

        if trail_draw:
            body.trail_control()

        body.draw(Camera)

    #text render
    if help_window:
        Text_controle.help_textRender()
    else:
        Text_controle.function_textRender()
        if follow:
            Text_controle.planet_characteristics(planet_list[followObj])
        else:
            Text_controle.baseTextRender()

    #key and other function control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_MINUS:
                if Camera.scale > 1:
                    Camera.scale -= Camera.speed_of_scale
                elif Camera.scale > 0:
                    Camera.scale -= Camera.speed_of_scale/10
            if event.key == pygame.K_EQUALS:
                if Camera.scale >= 1:
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

            #Time control
            if event.key == pygame.K_q:
                if Engine.time_speed > 1:
                    Engine.time_speed -= 1

            if event.key == pygame.K_e:
                Engine.time_speed += 1

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

    #print("________________")
    pygame.display.update()
    frames+=1
    time.sleep(0.01)