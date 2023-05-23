import pygame
from pygame.locals import *
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self, initial_position, size):

        global overall_speed
        global ground_height
        global screen_height

        pygame.sprite.Sprite.__init__(self)
        self.go_state = 1
        self.anim_speed = 5
        self.anim_cooldown = self.anim_speed
        self.image = pygame.image.load('player_' + str(self.go_state) + '.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.size = size
        self.jumping = False
        self.jumpheight = 250
        self.anim_air = False
        self.speed = 4 * overall_speed

    def update(self):

        global floor
        global player_slow_time
        global player_powerup_anim

        if player_slow_time > 0:
            self.speed = overall_speed
        else:
            self.speed = 4 * overall_speed

        self.anim_cooldown -= 1

        # jumping up
        if self.jumping:
            if self.rect.top >= screen_height - self.jumpheight:
                self.rect.top -= self.speed
            else:
                self.jumping = False

        # always falling down
        colide = False
        if pygame.sprite.collide_rect(self, floor):
            colide = True

        if (not self.jumping) & (not colide):
            self.rect.top += self.speed
            self.anim_air = False

        if self.anim_cooldown < 0:
            self.go_state += 1
            if self.go_state > 4:
                self.go_state = 1

            if self.anim_air:
                if player_powerup_anim > 0:
                    self.image = player_jump_powerup
                else:
                    self.image = player_jump
            else:
                if player_powerup_anim > 0:
                    if self.go_state == 1:
                        self.image = player_1_powerup
                    if self.go_state == 2:
                        self.image = player_2_powerup
                    if self.go_state == 3:
                        self.image = player_3_powerup
                    if self.go_state == 4:
                        self.image = player_4_powerup
                else:
                    if self.go_state == 1:
                        self.image = player_1
                    if self.go_state == 2:
                        self.image = player_2
                    if self.go_state == 3:
                        self.image = player_3
                    if self.go_state == 4:
                        self.image = player_4

            self.anim_cooldown = self.anim_speed

    def jump(self):
        if not self.jumping:
            self.anim_air = True
            self.jumping = True
            self.jumpheight = 800  # Increase the jump height


class Floor(pygame.sprite.Sprite):
    def __init__(self, groundcolor, initial_position, size):
        global powerups
        global obstacles
        global screen_width
        global screen_height
        global ground_height
        global player_size
        global overall_speed
        global spaceobjs

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.speed = 3 * overall_speed
         # Fill the surface with transparent color
        self.image.fill((0, 0, 0, 0))
    def update(self):
        global obstacle_cooldown

        powerups.update()
        obstacles.update()
        spaceobjs.update()

        obstacle_cooldown -= 1

        # add spaceobjs
        if randint(0, 100) == 0:
            spaceobj_initial_pos = (screen_width, screen_height - ground_height - randint(200, screen_height))
            spaceobjs.add(Spaceobj(spaceobj_initial_pos, self.speed))

        # add powerups
        if randint(0, 60) == 0:
            powerup_typ = randint(1, 4)
            powerup_initial_pos = (screen_width, screen_height - ground_height - powerup2_size - 5 - randint(0, 200))
            powerups.add(Powerup(powerup_typ, powerup_initial_pos, self.speed))

        # add obstacles
        if (obstacle_cooldown < 0) & (randint(0, 50) == 0):
            obstacle_size = (randint(30, 80), randint(30, 80))
            obstacle_initial_pos = (screen_width, screen_height - ground_height - obstacle_size[1] - randint(0, 200))
            obstacle = Obstacle(obstacle_initial_pos, obstacle_size, self.speed)
            if not pygame.sprite.spritecollideany(obstacle, powerups):
                obstacles.add(obstacle)
            else:
                obstacle.kill()
            obstacle_cooldown = 60 / overall_speed


class Powerup(pygame.sprite.Sprite):
    def __init__(self, typ, initial_position, speed):
        global background_color
        global powerup1_color
        global powerup2_color
        global powerup3_color
        global powerup4_color
        global powerup1_size
        global powerup2_size

        pygame.sprite.Sprite.__init__(self)

        if typ == 1:
            self.image = pygame.Surface((powerup1_size, powerup1_size))
            self.image.fill(background_color)
            self.image.set_colorkey(background_color)
            pygame.draw.circle(self.image, powerup1_color, (powerup1_size / 2, powerup1_size / 2), powerup1_size / 2, 0)
        if typ == 2:
            self.image = pygame.Surface((powerup2_size, powerup2_size))
            self.image.fill(background_color)
            self.image.set_colorkey(background_color)
            pygame.draw.circle(self.image, powerup2_color, (powerup2_size / 2, powerup2_size / 2), powerup2_size / 2, 0)
        if typ == 3:
            self.image = pygame.Surface((powerup1_size, powerup1_size))
            self.image.fill(background_color)
            self.image.set_colorkey(background_color)
            pygame.draw.circle(self.image, powerup3_color, (powerup1_size / 2, powerup1_size / 2), powerup1_size / 2, 0)
        if typ == 4:
            self.image = pygame.Surface((powerup1_size, powerup1_size))
            self.image.fill(background_color)
            self.image.set_colorkey(background_color)
            pygame.draw.circle(self.image, powerup4_color, (powerup1_size / 2, powerup1_size / 2), powerup1_size / 2, 0)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.typ = typ
        self.speed = speed
        self.rect.top -= 100  # Increase the height of the powerups

    def update(self):

        if (self.rect.left + powerup2_size) < 0:
            self.kill()

        global score
        global player
        global sound1
        global sound2
        global sound3
        global sound4
        global player_invincible_time
        global player_slow_time
        global player_powerup_anim

        self.rect.left -= self.speed
        if pygame.sprite.collide_rect(self, player):

            if self.typ == 1:
                player_powerup_anim = 0.5 * fps * overall_speed
                sound1.play()
                score += 1
            if self.typ == 2:
                player_powerup_anim = 1 * fps * overall_speed
                sound3.play()
                score += 5
            if self.typ == 3:
                player_slow_time = 4 * fps * overall_speed
                sound2.play()
            if self.typ == 4:
                player_invincible_time = 2 * fps * overall_speed
                sound4.play()

            self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, initial_position, size, speed):
        global obstacle_color

        pygame.sprite.Sprite.__init__(self)
        self.image = obstacle_image
       # self.image.fill(obstacle_color)
        self.rect = self.image.get_rect()  
        self.rect.topleft = initial_position
        self.speed = speed
        self.size = size

    def update(self):

        if (self.rect.left + self.size[0]) < 0:
            self.kill()

        global game_over
        global game_over_sound
        global player_invincible_time
        global game_over_anim
        global game_over_rect
        global game_over_rect_center

        self.rect.left -= self.speed
        if (player_invincible_time < 0) & pygame.sprite.collide_rect(self, player):
            game_over_sound.play()
            game_over_anim = 1 * fps * overall_speed
            game_over_rect = self
            game_over_rect_center = self.rect.center
            game_over = True


class Spaceobj(pygame.sprite.Sprite):
    def __init__(self, initial_position, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('spaceobj' + str(randint(1, 2)) + '.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.speed = speed

    def update(self):
        if (self.rect.left + self.image.get_width()) < 0:
            self.kill()

        self.rect.left -= self.speed


pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Zero Base 1")

# static values

overall_speed = 2.5

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
game_screen = pygame.display.set_mode((screen_width, screen_height), FULLSCREEN)
powerup1_size = 25
powerup2_size = 40
ground_height = 200
player_size = (25, 50)
 
score = 0
background_image = pygame.image.load("background.png")

background_color = (133, 182, 226)
text_color=(0, 178, 255)
ground_color = ( 0)  # Transparent ground color
powerup1_color = (237, 235, 0)  # 1pt
powerup2_color = (217, 53, 114)  # 5pts
powerup3_color = (0, 0, 0)  # slow player
powerup4_color = (255, 255, 255)  # invincible
obstacle_image = pygame.image.load("obstacle.png")
obstacle_color = (0,0,0)

fps = 60
game_over = False
game_started = False

myfont = pygame.font.Font('conthrax-sb.otf', 30)
logo = pygame.font.Font('conthrax-sb.otf', 120)
startendfont = pygame.font.Font('conthrax-sb.otf', 70)
game_over_sound = pygame.mixer.Sound("game_over.wav")
sound1 = pygame.mixer.Sound("sound1.wav")
sound2 = pygame.mixer.Sound("sound2.wav")
sound3 = pygame.mixer.Sound("sound3.wav")
sound4 = pygame.mixer.Sound("sound4.wav")

screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

player_jump = pygame.image.load('player_jump.png').convert_alpha()
player_jump_powerup = pygame.image.load('player_jump_powerup.png').convert_alpha()
player_1 = pygame.image.load('player_1.png').convert_alpha()
player_1_powerup = pygame.image.load('player_1_powerup.png').convert_alpha()
player_2 = pygame.image.load('player_2.png').convert_alpha()
player_2_powerup = pygame.image.load('player_2_powerup.png').convert_alpha()
player_3 = pygame.image.load('player_3.png').convert_alpha()
player_3_powerup = pygame.image.load('player_3_powerup.png').convert_alpha()
player_4 = pygame.image.load('player_4.png').convert_alpha()
player_4_powerup = pygame.image.load('player_4_powerup.png').convert_alpha()

####################

space_cooldown = 0
obstacle_cooldown = 0
game_over_anim = 0
player_invincible_time = 0
player_slow_time = 0
player_powerup_anim = 0
game_over_rect = None
game_over_rect_center = None

player = Player(
    ((screen_width / 2) - (player_size[0] / 2), screen_height - player_size[1] - ground_height),
    player_size)

floor = Floor(ground_color, (0, screen_height - ground_height), (screen_width, ground_height))

powerups = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
spaceobjs = pygame.sprite.Group()

clock = pygame.time.Clock()

pygame.mixer.music.load('zerobase1_bgm.wav')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)

while True:
    time_passed = clock.tick(fps)
    keys = pygame.key.get_pressed()
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    if keys[K_ESCAPE]:
        exit()

    game_over_anim -= 1

    if game_over_anim > 0:
        
        game_over_rect.image = pygame.Surface(((game_over_rect.rect.width + 10), (game_over_rect.rect.height + 10)))
        game_over_rect.image.fill(obstacle_color)
        game_over_rect.rect = game_over_rect.image.get_rect()
        game_over_rect.rect.center = game_over_rect_center
         
        screen.blit(floor.image, floor.rect)
        spaceobjs.draw(screen)
       
        screen.blit(player.image, player.rect)

        powerups.draw(screen)
        obstacles.draw(screen)

    else:
        if game_started & (not game_over):

            space_cooldown -= 1
            player_invincible_time -= 1
            player_slow_time -= 1
            player_powerup_anim -= 1

            if keys[K_SPACE] & (space_cooldown < 0):
                player.jump()
                space_cooldown = 70 / overall_speed

            floor.update()
            screen.blit(floor.image, floor.rect)
            spaceobjs.draw(screen)

            player.update()
            screen.blit(player.image, player.rect)

            powerups.draw(screen)
            obstacles.draw(screen)

            screen.blit(myfont.render("Score: " + str(score), 1, text_color), (screen_width - 320, 0))

            if player_slow_time > 0:
                screen.blit(myfont.render("Slow: " + str(player_slow_time), 1, powerup1_color), (screen_width - 320, 25))
            if player_invincible_time > 0:
                screen.blit(myfont.render("Invincible: " + str(player_invincible_time), 1, powerup1_color),
                            (screen_width - 320, 50))
        else:
            if game_over:
                for obstacle in obstacles:
                    obstacle.kill()
                screen.fill(obstacle_color)
                
                screen.blit(startendfont.render("Game Over", 1, powerup1_color), (80, (screen_height / 2) - 100 - 40))
                screen.blit(startendfont.render("Score: " + str(score), 1, text_color),
                            (80, (screen_height / 2) - 40))
                screen.blit(startendfont.render("Press ENTER for new game", 1, text_color),
                            (80, (screen_height / 2) + 100 - 40))
                if keys[K_RETURN]:
                    obstacles.empty()
                    powerups.empty()
                    score = 0
                    space_cooldown = 0
                    obstacle_cooldown = 0
                    player_invincible_time = 0
                    player_slow_time = 0
                    player_powerup_anim = 0
                    game_over = False

            if not game_started:
                screen.blit(logo.render("ZERO BASE ", 1, text_color), (220, (screen_height / 2) - 300))
                screen.blit(logo.render("001 ", 1, powerup1_color), (500, (screen_height / 2) - 180))
                screen.blit(startendfont.render("ENTER to start", 1, text_color), (120, (screen_height / 2) + 20))
                screen.blit(startendfont.render("SPACE for jumping", 1, text_color),
                            (120, (screen_height / 2) + 100))
                #screen.blit(startendfont.render("Power-Up Instructions:", 1, text_color),
                           # (120, (screen_height / 2) + 180))
                if keys[K_RETURN]:
                    game_started = True
    pygame.mixer.music.get_busy()
    pygame.display.update()
 