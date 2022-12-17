import pygame
import sys
from settings import *
from player import Player
from car import Car


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.bg = pygame.image.load('../graphics/main/map.png').convert()
        self.fg = pygame.image.load('../graphics/main/overlay.png').convert_alpha()

    def customize_draw(self):

        # change the offset vector
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        # blit the bg
        display_surf.blit(self.bg, -self.offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            display_surf.blit(sprite.image, offset_pos)

        display_surf.blit(self.fg, -self.offset)


# Basic setup
pygame.init()
display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Frogger')
clock = pygame.time.Clock()

# Groups
all_sprites = AllSprites()

# Sprites
player = Player((500, 200), all_sprites)
car = Car((1000, 200), all_sprites)

while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Delta time
    dt = clock.tick() / 1000

    # draw bg
    display_surf.fill('black')

    # Update
    all_sprites.update(dt)

    # Graphics
    all_sprites.customize_draw()

    # Drawing the frame
    pygame.display.update()
