import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_surface_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_surface_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk_surfaces = [player_walk_surface_1, player_walk_surface_2]
        self.player_index = 0
        self.player_jump_surface = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk_surfaces[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump_surface
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk_surfaces):
                self.player_index = 0
            self.image = self.player_walk_surfaces[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'Fly':
            fly_1_surface = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2_surface = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.surfaces = [fly_1_surface, fly_2_surface]
            y_position = 210
        else:
            snail_1_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2_surface = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.surfaces = [snail_1_surface, snail_2_surface]
            y_position = 300

        self.animation_index = 0
        self.image = self.surfaces[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_position))
    
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.surfaces):
            self.animation_index = 0
        self.image = self.surfaces[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()


def game_seconds():
    return int(pygame.time.get_ticks() / 1000)

def display_score():
    current_time = game_seconds() - game_time_delta
    score_surface = pixel_font.render(f'Score: {current_time}', False, '#404040')
    score_rectangle = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rectangle)
    return current_time
    
def collision():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    return True

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Pixel Jumper')
clock = pygame.time.Clock()
pixel_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
game_time_delta = 0
player_score = 0
background_music = pygame.mixer.Sound('audio/music.wav')
background_music.set_volume(0.05)
background_music.play(loops = -1)

# Environment
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/Ground.png').convert()

# Sprites
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# Introduction screen
player_stand_surface = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand_surface = pygame.transform.rotozoom(player_stand_surface, 0, 2)
player_stand_rectangle = player_stand_surface.get_rect(center = (400, 200))

game_name_surface = pixel_font.render('Pixel Jumper', False, (111, 196, 169))
game_name_rectangle = game_name_surface.get_rect(center = (400, 80))

game_message_surface = pixel_font.render('Press space to start', False, (111, 196, 169))
game_message_rectangle = game_message_surface.get_rect(center = (400, 330))

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 300)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['Fly', 'Snail', 'Snail', 'Snail'])))
        else: 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                game_time_delta = game_seconds()


    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        player_score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision()
    else:
        background_music.fadeout(400)
        screen.fill((94, 129, 162))
        screen.blit(player_stand_surface, player_stand_rectangle)

        score_message_surface = pixel_font.render(f'Score: {player_score}', False, (111, 196, 169))
        score_message_rectangle = score_message_surface.get_rect(center = (400, 330))

        screen.blit(game_name_surface, game_name_rectangle)

        if player_score:
            screen.blit(score_message_surface, score_message_rectangle)
        else:
            screen.blit(game_message_surface, game_message_rectangle)


    pygame.display.update()
    clock.tick(60)