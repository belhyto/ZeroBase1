import pygame
from pygame.locals import *
from random import randint

# Player class represents the player character
class Player(pygame.sprite.Sprite):
    def __init__(self, initial_position, size):
        # Global variables
        global overall_speed   # Overall speed of the game
        global ground_height    # Height of the ground/floor
        global screen_height    # Height of the game screen

        pygame.sprite.Sprite.__init__(self)
        self.go_state = 1   # Current animation state of the player
        self.anim_speed = 5 # Speed of animation
        self.anim_cooldown = self.anim_speed    # Cooldown between animation frames
        self.image = pygame.image.load('player_' + str(self.go_state) + '.png').convert_alpha()  # Load player image
        self.rect = self.image.get_rect()    # Rectangle representing player's position and size
        self.rect.topleft = initial_position    # Initial position of the player
        self.size = size # Size of the player
        self.jumping = False    # Flag indicating if the player is currently jumping
        self.jumpheight = 250   # Height of the jump
        self.anim_air = False   # Flag indicating if the player is in the air
        self.speed = 4 * overall_speed  # Speed of the player

    def update(self):
        # Global variables
        global floor  # Object representing the floor/ground
        global player_slow_time  # Duration of slow time power-up
        global player_powerup_anim  # Duration of power-up animation

        # Adjust speed based on power-ups and slow time
        if player_slow_time > 0:
            self.speed = overall_speed  # Slow time power-up active, adjust speed
        else:
            self.speed = 4 * overall_speed  # Normal speed

        self.anim_cooldown -= 1  # Decrease the animation cooldown

        # Jumping up
        if self.jumping:
            if self.rect.top >= screen_height - self.jumpheight:
                self.rect.top -= self.speed  # Move player upwards
            else:
                self.jumping = False  # Reached the maximum jump height

        # Always falling down
        collide = False
        if pygame.sprite.collide_rect(self, floor):
            collide = True  # Check if player collides with the floor

        if (not self.jumping) & (not collide):
            self.rect.top += self.speed  # Move player downwards
            self.anim_air = False  # Player is not in the air

        if self.anim_cooldown < 0:
            self.go_state += 1  # Switch to the next animation state
            if self.go_state > 4:
                self.go_state = 1  # Reset animation state

            if self.anim_air:
                if player_powerup_anim > 0:
                    self.image = player_jump_powerup  # Set player image for jump with power-up
                else:
                    self.image = player_jump  # Set player image for jump without power-up
            else:
                if player_powerup_anim > 0:
                    if self.go_state == 1:
                        self.image = player_1_powerup  # Set player image for running with power-up (state 1)
                    if self.go_state == 2:
                        self.image = player_2_powerup  # Set player image for running with power-up (state 2)
                    if self.go_state == 3:
                        # Set player image for running with power-up (state 3)
                        self.image = player_3
                    if self.go_state == 4:
                        self.image = player_4

            self.anim_cooldown = self.anim_speed

    def jump(self):
        if not self.jumping:
            self.anim_air = True  # Flag to indicate player is in the air
            self.jumping = True  # Set jumping flag to True
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
        self.image.set_alpha(0)  # Set the transparency of the surface to 0
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position  # Set the initial position of the floor
        self.speed = 3 * overall_speed  # Set the speed of the floor

        # Fill the surface with transparent color
        self.image.fill((0, 0, 0, 0))
    def update(self):
        global obstacle_cooldown

        powerups.update()  # Update the powerups sprite group
        obstacles.update()  # Update the obstacles sprite group
        spaceobjs.update()  # Update the spaceobjs sprite group

        obstacle_cooldown -= 1  # Decrease the obstacle cooldown

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
            # If the powerup is off the screen, remove it from the game
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

        self.rect.left -= self.speed # Move the powerup towards the left
        if pygame.sprite.collide_rect(self, player):
        # If the powerup collides with the player
            if self.typ == 1:
                # Powerup type 1: Increase player_powerup_anim, play sound1, and increase the score
                player_powerup_anim = 0.5 * fps * overall_speed
                sound1.play()
                score += 1
            if self.typ == 2:
                # Powerup type 2: Increase player_powerup_anim, play sound3, and increase the score
                player_powerup_anim = 1 * fps * overall_speed
                sound3.play()
                score += 5
            if self.typ == 3:
                # Powerup type 3: Set player_slow_time, play sound2
                player_slow_time = 4 * fps * overall_speed
                sound2.play()
            if self.typ == 4:
                # Powerup type 4: Set player_invincible_time, play sound4
                player_invincible_time = 2 * fps * overall_speed
                sound4.play()

            self.kill() # Remove the powerup from the game


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, initial_position, size, speed):
        global obstacle_color # Global variable for obstacle color

        pygame.sprite.Sprite.__init__(self)  # Initialize the parent class
        self.image = obstacle_image  # Set the image for the obstacle
        self.rect = self.image.get_rect()   # Get the rectangle of the obstacle image
        self.rect.topleft = initial_position # Set the initial position of the obstacle
        self.speed = speed # Set the speed of the obstacle
        self.size = size # Set the size of the obstacle

    def update(self):

        if (self.rect.left + self.size[0]) < 0:
            self.kill()  # Kill the obstacle if it goes off the screen

        global game_over  # Global variable for game over
        global game_over_sound  # Global variable for game over sound
        global player_invincible_time  # Global variable for player invincible time
        global game_over_anim  # Global variable for game over animation
        global game_over_rect  # Global variable for game over rectangle
        global game_over_rect_center  # Global variable for game over rectangle center

        self.rect.left -= self.speed  # Move the obstacle to the left
        if (player_invincible_time < 0) & pygame.sprite.collide_rect(self, player):
            # Check collision between obstacle and player when player is not invincible
            game_over_sound.play()  # Play the game over sound
            game_over_anim = 1 * fps * overall_speed  # Set game over animation duration
            game_over_rect = self  # Set the game over rectangle to the obstacle
            game_over_rect_center = self.rect.center  # Set the game over rectangle center
            game_over = True  # Set the game over flag


class Spaceobj(pygame.sprite.Sprite):
    def __init__(self, initial_position, speed):
        pygame.sprite.Sprite.__init__(self)  # Initialize the parent class
        self.image = pygame.image.load('spaceobj' + str(randint(1, 2)) + '.png').convert_alpha()
        # Load a random space object image
        self.rect = self.image.get_rect()  # Get the rectangle of the space object image
        self.rect.topleft = initial_position  # Set the initial position of the space object
        self.speed = speed  # Set the speed of the space object

    def update(self):
        if (self.rect.left + self.image.get_width()) < 0:
            self.kill()  # Kill the space object if it goes off the screen

        self.rect.left -= self.speed  # Move the space object to the left


pygame.init()  # Initialize Pygame
pygame.mixer.init()  # Initialize the mixer for sound
pygame.display.set_caption("Zero Base 1")  # Set the window caption to "Zero Base 1"

# static values

overall_speed = 2.5  # Overall speed of the game

screen_info = pygame.display.Info()  # Get information about the display/screen
screen_width = screen_info.current_w  # Get the current width of the screen
screen_height = screen_info.current_h  # Get the current height of the screen
game_screen = pygame.display.set_mode((screen_width, screen_height), FULLSCREEN)  # Set the game screen to fullscreen
powerup1_size = 25  # Size of powerup 1
powerup2_size = 40  # Size of powerup 2
ground_height = 200  # Height of the ground
player_size = (25, 50)  # Size of the player

score = 0  # Score variable
background_image = pygame.image.load("background.png")  # Load the background image

background_color = (133, 182, 226)  # Background color
text_color = (0, 178, 255)  # Color of text
ground_color = (0)  # Transparent ground color
powerup1_color = (237, 235, 0)  # Color of powerup 1
powerup2_color = (217, 53, 114)  # Color of powerup 2
powerup3_color = (0, 0, 0)  # Color of powerup 3
powerup4_color = (255, 255, 255)  # Color of powerup 4
obstacle_image = pygame.image.load("obstacle.png")  # Load the obstacle image
obstacle_color = (0, 0, 0)  # Color of the obstacle

fps = 60  # Frames per second
game_over = False  # Game over flag
game_started = False  # Game started flag

myfont = pygame.font.Font('conthrax-sb.otf', 30)  # Font for general text
logo = pygame.font.Font('conthrax-sb.otf', 120)  # Font for logo
startendfont = pygame.font.Font('conthrax-sb.otf', 70)  # Font for start/end text
game_over_sound = pygame.mixer.Sound("game_over.wav")  # Sound for game over
sound1 = pygame.mixer.Sound("sound1.wav")  # Sound 1
sound2 = pygame.mixer.Sound("sound2.wav")  # Sound 2
sound3 = pygame.mixer.Sound("sound3.wav")  # Sound 3
sound4 = pygame.mixer.Sound("sound4.wav")  # Sound 4

screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)  # Create the game screen

player_jump = pygame.image.load('player_jump.png').convert_alpha()  # Load player jump image
player_jump_powerup = pygame.image.load('player_jump_powerup.png').convert_alpha()  # Load player jump powerup image
player_1 = pygame.image.load('player_1.png').convert_alpha()  # Load player 1 image
player_1_powerup = pygame.image.load('player_1_powerup.png').convert_alpha()  # Load player 1 powerup image
player_2 = pygame.image.load('player_2.png').convert_alpha()  # Load player 2 image
player_2_powerup = pygame.image.load('player_2_powerup.png').convert_alpha()  # Load player 2 powerup image
player_3 = pygame.image.load('player_3.png').convert_alpha()  # Load player 3 image
player_3_powerup = pygame.image.load('player_3_powerup.png').convert_alpha()
player_4 = pygame.image.load('player_4.png').convert_alpha()
player_4_powerup = pygame.image.load('player_4_powerup.png').convert_alpha()
####################

space_cooldown = 0  # Cooldown for space powerup
obstacle_cooldown = 0  # Cooldown for obstacles
game_over_anim = 0  # Animation for game over
player_invincible_time = 0  # Time for player invincibility
player_slow_time = 0  # Time for player slowness
player_powerup_anim = 0  # Animation for player powerup
game_over_rect = None  # Rectangular area for game over
game_over_rect_center = None  # Center of the game over rectangle

player = Player(
    ((screen_width / 2) - (player_size[0] / 2), screen_height - player_size[1] - ground_height),
    player_size)  # Create player object with initial position and size

floor = Floor(ground_color, (0, screen_height - ground_height), (screen_width, ground_height))  # Create floor object

powerups = pygame.sprite.Group()  # Group for powerups
obstacles = pygame.sprite.Group()  # Group for obstacles
spaceobjs = pygame.sprite.Group()  # Group for space objects

clock = pygame.time.Clock()  # Create a clock object for managing the game's frame rate

pygame.mixer.music.load('zerobase1_bgm.wav')  # Load the background music
pygame.mixer.music.set_volume(0.5)  # Set the volume of the background music
pygame.mixer.music.play(loops=-1)  # Start playing the background music in a loop

while True:  # Main game loop
    time_passed = clock.tick(fps)  # Get the time passed since the last frame and limit the frame rate
    keys = pygame.key.get_pressed()  # Get the currently pressed keys
    screen.blit(background_image, (0, 0))  # Draw the background image on the screen

    for event in pygame.event.get():  # Process events
        if event.type == QUIT:  # If the event is quit, exit the game
            exit()

    if keys[K_ESCAPE]:  # If the Escape key is pressed, exit the game
        exit()

    game_over_anim -= 1  # Decrement the game over animation count


    if game_over_anim > 0: # If the game over animation is still playing
        # Update the game over rectangle
        game_over_rect.image = pygame.Surface(((game_over_rect.rect.width + 10), (game_over_rect.rect.height + 10)))
        game_over_rect.image.fill(obstacle_color)
        game_over_rect.rect = game_over_rect.image.get_rect()
        game_over_rect.rect.center = game_over_rect_center
         
        screen.blit(floor.image, floor.rect)  # Draw the floor on the screen
        spaceobjs.draw(screen)  # Draw the space objects on the screen

        screen.blit(player.image, player.rect)  # Draw the player on the screen

        powerups.draw(screen)  # Draw the powerups on the screen
        obstacles.draw(screen)  # Draw the obstacles on the screen

    else:  # If the game over animation is not playing
        if game_started and (not game_over):  # If the game has started and is not over
            space_cooldown -= 1  # Decrease the space cooldown timer
            player_invincible_time -= 1  # Decrease the player invincibility time
            player_slow_time -= 1  # Decrease the player slowness time
            player_powerup_anim -= 1  # Decrease the player powerup animation time

            if keys[K_SPACE] & (space_cooldown < 0): # If the space key is pressed and the space cooldown is over, make the player jump
                player.jump()
                space_cooldown = 70 / overall_speed

            floor.update()  # Update the floor
            screen.blit(floor.image, floor.rect)  # Draw the floor on the screen
            spaceobjs.draw(screen)  # Draw the space objects on the screen

            player.update()  # Update the player
            screen.blit(player.image, player.rect)  # Draw the player on the screen

            powerups.draw(screen)  # Draw the powerups on the screen
            obstacles.draw(screen)  # Draw the obstacles on the screen

            screen.blit(myfont.render("Score: " + str(score), 1, text_color), (screen_width - 320, 0))

            if player_slow_time > 0:
                screen.blit(myfont.render("Slow: " + str(player_slow_time), 1, powerup1_color), (screen_width - 320, 25))
            if player_invincible_time > 0:
                screen.blit(myfont.render("Invincible: " + str(player_invincible_time), 1, powerup1_color),
                            (screen_width - 320, 50))
        else:  # If the game is not started or is over

            if game_over:  # If the game is over
                for obstacle in obstacles:  # Remove all obstacles from the screen
                    obstacle.kill()
                screen.fill(obstacle_color)  # Fill the screen with the obstacle color
                # Display the game over message and score
                screen.blit(startendfont.render("Game Over", 1, powerup1_color), (80, (screen_height / 2) - 100 - 40))
                screen.blit(startendfont.render("Score: " + str(score), 1, text_color),
                             (80, (screen_height / 2) - 40))
                screen.blit(startendfont.render("Press ENTER for new game", 1, text_color),
                            (80, (screen_height / 2) + 100 - 40))
                if keys[K_RETURN]:  # If the return key is pressed
                    obstacles.empty()  # Empty the obstacles group
                    powerups.empty()  # Empty the powerups group
                    score = 0  # Reset the score to 0
                    space_cooldown = 0  # Reset the space cooldown
                    obstacle_cooldown = 0  # Reset the obstacle cooldown
                    player_invincible_time = 0  # Reset the player invincibility time
                    player_slow_time = 0  # Reset the player slowness time
                    player_powerup_anim = 0  # Reset the player powerup animation time
                    game_over = False  # Set game_over flag to False

                if not game_started:  # If the game is not started
                     screen.blit(logo.render("ZERO BASE ", 1, text_color), (220, (screen_height / 2) - 300))  # Display the game logo
                     screen.blit(logo.render("001 ", 1, powerup1_color), (500, (screen_height / 2) - 180))  # Display the game version
                     screen.blit(startendfont.render("ENTER to start", 1, text_color), (120, (screen_height / 2) + 20))  # Display start instructions
                     screen.blit(startendfont.render("SPACE for jumping", 1, text_color), (120, (screen_height / 2) + 100))  # Display jump instructions
                #screen.blit(startendfont.render("Power-Up Instructions:", 1, text_color),
                           # (120, (screen_height / 2) + 180))
                if keys[K_RETURN]:  # If the return key is pressed
                    game_started = True  # Start the game
    pygame.mixer.music.get_busy()  # Check if the background music is still playing
    pygame.display.update()  # Update the display