import pygame
import sys
from settings import *
from player import Player
from car import Car
from random import choice, randint
from sprite import SimpleSprite, LongSprite


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
obstacle_sprites = pygame.sprite.Group()

# Sprites
player = Player((2062, 3274), all_sprites, obstacle_sprites)

# Timer
car_timer = pygame.event.custom_type()
pygame.time.set_timer(car_timer, 50)
pos_list = []

# Font
font = pygame.font.Font(None, 50)
win_text_surf = font.render('You have won the game!', True, 'gold')
win_text_rect = win_text_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

# Music
bg_music = pygame.mixer.Sound('../audio/music.mp3')
bg_music.play(loops=-1)

# Sprite setup

# Simple sprites
for file_name, pos_list in SIMPLE_OBJECTS.items():
    path = f'../graphics/objects/simple/{file_name}.png'
    surf = pygame.image.load(path).convert_alpha()
    for pos in pos_list:
        SimpleSprite(surf, pos, [all_sprites, obstacle_sprites])

# Long sprites
for file_name, pos_list in LONG_OBJECTS.items():
    path = f'../graphics/objects/long/{file_name}.png'
    surf = pygame.image.load(path).convert_alpha()
    for pos in pos_list:
        LongSprite(surf, pos, [all_sprites, obstacle_sprites])

# Game loop
while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == car_timer:
            random_pos = choice(CAR_START_POSITIONS)
            if random_pos not in pos_list:
                pos_list.append(random_pos)
                pos = (random_pos[0], random_pos[1] + randint(-8, 8))
                Car(pos, [all_sprites, obstacle_sprites])
            if len(pos_list) > 5:
                del pos_list[0]

    # Delta time
    dt = clock.tick() / 1000

    if player.pos.y > 1180:
        # Update
        all_sprites.update(dt)

        # Graphics
        all_sprites.customize_draw()
    else:

        # draw bg
        display_surf.fill('black')

        # Draw text
        display_surf.blit(win_text_surf, win_text_rect)

# Drawing the frame
    pygame.display.update()
