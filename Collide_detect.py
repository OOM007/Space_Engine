import pygame
import math

response_coef = 0.75

class Collide:
    def collision(self, obj1, obj2):
        collision_axis = obj1.position - obj2.position
        dist_2 = collision_axis.x**2 + collision_axis.y**2
        min_radius = obj1.size + obj2.size

        if (dist_2 < min_radius ** 2):
            dist = math.sqrt(dist_2)
            n = collision_axis/dist

            mass_ratio1 = obj1.mass / (obj1.mass + obj2.mass)
            mass_ratio2 = obj2.mass / (obj1.mass + obj2.mass)

            delta = 0.5 * response_coef * (dist - min_radius)

            obj1.position -= n*(mass_ratio2 * delta)
            obj2.position += n*(mass_ratio1 * delta)
            return True

    def collision_detect(self, obj1, obj2):
        dist = math.dist(obj1.position, obj2.position)
        radius = obj1.size + obj2.size

        if dist < radius:
            return True

    def collison_math(self, obj1, obj2):
        mass_sum = obj1.mass + obj2.mass
        vel1 = obj1.position - obj1.old_position
        vel2 = obj2.position - obj2.old_position

        if vel1-vel2 == 0:
            pass
        else:
            v1x = 0.9 * (vel1[0] * (obj1.mass - obj2.mass) + (2 * (obj2.mass * vel2[0]))) / mass_sum
            v1y = 0.9 * (vel1[1] * (obj1.mass - obj2.mass) + (2 * (obj2.mass * vel2[1]))) / mass_sum
            v2x = 0.9 * (vel2[0] * (obj2.mass - obj1.mass) + (2 * (obj1.mass * vel1[0]))) / mass_sum
            v2y = 0.9 * (vel2[1] * (obj2.mass - obj1.mass) + (2 * (obj1.mass * vel1[1]))) / mass_sum

            # v1t = (obj1.mass * vel1[0]) + (obj2.mass * vel2[0]) -
            v1 = pygame.Vector2(v1x, v1y)
            v2 = pygame.Vector2(v2x, v2y)

            obj1.old_position = obj1.position
            obj2.old_position = obj2.position

            obj1.position = obj1.position-v1
            obj2.position = obj2.position+v2

    def collide_body_stab(self, obj1, obj2):
        if self.collision_detect(obj1, obj2):
            axis = obj1.position - obj2.position

            overlap_x = axis.x - (obj1.size + obj2.size)
            overlap_y = axis.y - (obj1.size + obj2.size)

            if axis.x != 0:
                obj1.position.x = obj1.position.x - overlap_x * 0.5
                obj1.old_position.x = obj1.old_position.x - overlap_x * 0.5

                obj2.position.x = obj2.position.x + overlap_x * 0.5
                obj2.old_position.x = obj2.old_position.x + overlap_x * 0.5

            if axis.y != 0:
                obj1.position.y = obj1.position.y - overlap_y * 0.5
                obj1.old_position.y = obj1.old_position.y - overlap_y * 0.5

                obj2.position.y = obj2.position.y + overlap_y * 0.5
                obj2.old_position.y = obj2.old_position.y + overlap_y * 0.5