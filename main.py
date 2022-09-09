import pygame
import pygame.math as pmath
import math
import random
pygame.init()


SW = 800
SH = 800
screen = pygame.display.set_mode([SW, SH])
pygame.display.set_caption("Boids")
FPS = 60
clock = pygame.time.Clock()

flock = []


def main():
    init_flock(flock, 100)
    run = True
    while run:
        screen.fill((0,0,0))
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False
        draw_flock(flock)
        pygame.display.flip()
    pygame.quit()


def init_flock(arr, num):
    for i in range(num):
        b = Boid()
        arr.append(b)


def draw_flock(arr):
    for boid in arr:
        boid.update_flock(arr)
        boid.update()
        boid.show()


class Boid:
    def __init__(self):
        self.position = pmath.Vector2(random.randint(0,SW), random.randint(0,SH))
        self.velocity = pmath.Vector2(random.uniform(-1,1), random.uniform(-1,1))
        self.velocity.normalize()
        self.velocity = self.velocity * random.uniform(2, 4)
        self.acceleration = pmath.Vector2()
        self.color = (255,255,255)
        self.visionRadius = 50
        self.max_force = .5
        self.max_speed = 4

    def show(self):
        pygame.draw.circle(screen, self.color, self.position, 5)

    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration
        self.limit(self.velocity, self.max_speed)
        self.wrap()

    def limit(self, vector, max_length):
        squared_mag = vector.magnitude() * vector.magnitude()
        if squared_mag > (max_length * max_length):
            vector.x = vector.x / math.sqrt(squared_mag)
            vector.y = vector.y / math.sqrt(squared_mag)
            vector.x = vector.x * max_length
            vector.y = vector.y * max_length

    def wrap(self):
        if self.position.x > SW:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = SW
        if self.position.y > SH:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = SH

    def align(self, others):
        average = pmath.Vector2()
        total = 0
        for other in others:
            dist = self.position.distance_to(other.position)
            if dist <= self.visionRadius and other is not self:
                other_velocity = other.velocity.normalize()
                average += other_velocity
                total+=1
        if total > 0:
            average /= total
            average.normalize()
            average *= self.max_speed
            average -= self.velocity
            average.scale_to_length(self.max_force)
        return average

    def cohese(self, others):
        average = pmath.Vector2()
        total = 0
        for other in others:
            dist = self.position.distance_to(other.position)
            if dist <= self.visionRadius and other is not self:
                average += other.position
                total+=1
        if total > 0:
            average /= total
            average -= self.position
            average.normalize()
            average *= self.max_speed
            average -= self.velocity
            average.scale_to_length(self.max_force)
        return average

    def update_flock(self, arr):
        # alignment = self.align(arr)
        cohesion = self.cohese(arr)
        # self.acceleration = alignment
        self.acceleration = cohesion

if __name__ == '__main__':
    main()