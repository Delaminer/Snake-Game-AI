# Tutorial: https://realpython.com/pygame-a-primer/

# Set up PyGame
import pygame
pygame.init()

# Set up game window
screen = pygame.display.set_mode([500, 500])

# Run the game until the user quits
running = True
while running:
    
    #Check for user closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Color background white
    screen.fill([255, 255, 255])

    # Draw a blue circle
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Flip the display (showing the new screen)
    pygame.display.flip()

# Quit the program
pygame.quit()