# Tutorial: https://realpython.com/pygame-a-primer/

# Import random for random numbers
import random

# Set up PyGame
import pygame

# Import keyboard input
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

# Set up game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Set up a clock to control frame rate
clock = pygame.time.Clock()

# Define a player object which extends PyGame's sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # self.surf = pygame.Surface((75, 25))
        # self.surf.fill((0, 255, 0))
        self.surf = pygame.image.load("jet.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        # Move the player based on input
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep the player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Define an enemy object which extends PyGame's sprite class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        # self.surf = pygame.Surface((20, 10))
        # self.surf.fill((255, 0, 0))
        self.surf = pygame.image.load("missile.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the enemy based on its speed
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Define a cloud background 
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert_alpha()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
    
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

# Create a custom event for adding enemies
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
# Create a custom event for adding clouds
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Create the player
player = Player()

# Create sprite groups to hold all of the enemies, all of the clouds, and all of the sprites
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Run the game until the user quits
running = True
while running:
    
    # Check for user closing the window
    for event in pygame.event.get():
        # Check if user pressed a key
        if event.type == KEYDOWN:
            # Check if it was the escape key (close the window if so)
            if event.key == K_ESCAPE:
                running = False

        # Check if user closed the window
        elif event.type == pygame.QUIT:
            running = False

        # Check if the addenemy event triggered
        elif event.type == ADDENEMY:
            # Create a new enemy and add it to the groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Check if the addcloud event triggered
        elif event.type == ADDCLOUD:
            # Create a new enemy and add it to the groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
    

    # Get the set of keys pressed
    pressed_keys = pygame.key.get_pressed()
    # Check user input
    player.update(pressed_keys)

    # Update enemies
    enemies.update()
    # Update clouds
    clouds.update()

    # Color background sky blue
    screen.fill((135, 206, 250))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check for a collision between an enemy and the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, remove the player and stop the game
        player.kill()
        running = False

    # Flip the display (showing the new screen)
    pygame.display.flip()

    # Maintain the frame rate at 30 frames per second
    clock.tick(30)

# Quit the program
pygame.quit()