# For random numbers
import random

# Set up pygame
import pygame
from pygame import (
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

# Create the Player/Snake class
class Player():
    def __init__(self):
        super(Player, self).__init__()

        # Define the pieces of the snake
        self.pieces = []
        self.pieces.append([10, 10])
        # self.pieces.append([9, 10])
        # self.pieces.append([8, 10])

        # self.surf = pygame.Surface((20, 20))
        # self.surf.fill((0, 255, 0))
        self.surf = pygame.image.load('snake_piece.png').convert()

        self.direction = 1

        self.fruit = self.pieces[0]
        self.moveFruit()
        self.fruit_surf = pygame.image.load('fruit.png').convert_alpha()

        self.score = 0

    # This method moves the fruit to a spot where there is no snake
    def moveFruit(self):
        while self.fruit in self.pieces:
            self.fruit = [random.randint(0, 19), random.randint(0, 19)]

    def update(self, pressed_keys):
        # Change direction
        if pressed_keys[K_UP] and self.direction != 3:
            self.direction = 1
        if pressed_keys[K_DOWN] and self.direction != 1:
            self.direction = 3
        if pressed_keys[K_LEFT] and self.direction != 2:
            self.direction = 4
        if pressed_keys[K_RIGHT] and self.direction != 4:
            self.direction = 2

        # Move snake head
        headPiece = [self.pieces[-1][0], self.pieces[-1][1]]
        if self.direction == 1: # Up
            headPiece[1] -= 1
        elif self.direction == 2: # Right
            headPiece[0] += 1
        elif self.direction == 3: # Down
            headPiece[1] += 1
        elif self.direction == 4: # Left
            headPiece[0] -= 1
        
        # Check for collision with a wall or a piece of the snake (for a game over)
        if headPiece in self.pieces or headPiece[0] < 0 or headPiece[0] >= 20 or headPiece[1] < 0 or headPiece[1] >= 20:
            # Game over
            return True

        # Add the head piece
        self.pieces.append(headPiece)

        # Check for a fruit collision
        if self.fruit == self.pieces[-1]:
            # Collect fruit (not removing the last piece)
            self.moveFruit()
            self.score += 1
        else:
            # Remove the last piece
            del self.pieces[0]

        return False

    def getPosition(self, x, y):
        return (x * 20 + 200, y * 20 + 100)

    def draw(self, screen):
        # Draw snake pieces
        for x, y in self.pieces:
            screen.blit(self.surf, self.getPosition(x, y))

        # Draw fruit
        screen.blit(self.fruit_surf, self.getPosition(self.fruit[0], self.fruit[1]))



player = Player()

# Create the image of the board
board = pygame.image.load('board.png').convert()

# Create a font to display your score
font = pygame.font.SysFont('segoeui', 24)
# fonts = pygame.font.get_fonts()
# print(len(fonts))
# for f in fonts:
#     print(f)

running = True
# Main game loop
while running:
    for event in pygame.event.get():
        # User closes window
        if event.type == pygame.QUIT:
            running = False

    # Get user pressed keys
    pressed_keys = pygame.key.get_pressed()
    # Update player position
    if player.update(pressed_keys):
        # Game Over
        running = False

    # Color background with board
    screen.blit(board, (0, 0))

    # Draw player
    player.draw(screen)

    # Draw score
    text = 'Score: {}'.format(player.score)
    textImage = font.render(text, True, (0, 0, 0))
    screen.blit(textImage, (320, 30))

    # Output display
    pygame.display.flip()

    # Set frame rate
    clock.tick(8)

# Quit the program
pygame.quit()

print('Game Over! You scored {}.'.format(player.score))