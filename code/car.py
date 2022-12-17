import pygame
from os import walk
from random import choice


class Car(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        # Image setup
        self.car_choice()
        self.image = choice(self.car_images)
        self.rect = self.image.get_rect(center=pos)

        # Float based movement
        self.pos = pygame.math.Vector2(self.rect.center)

        if pos[0] < 300:
            self.direction = pygame.math.Vector2(1, 0)
        else:
            self.direction = pygame.math.Vector2(-1, 0)
            self.image = pygame.transform.flip(self.image, True, False)

        self.speed = 0

    def car_choice(self):
        self.car_images = []
        for img_path, _, img_list in walk('../graphics/cars'):
            for img in img_list:
                path = img_path + '/' + img
                surf = pygame.image.load(path).convert_alpha()
                self.car_images.append(surf)

    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        # Border check
        if -200 < self.rect.x > 3200:
            self.kill()
